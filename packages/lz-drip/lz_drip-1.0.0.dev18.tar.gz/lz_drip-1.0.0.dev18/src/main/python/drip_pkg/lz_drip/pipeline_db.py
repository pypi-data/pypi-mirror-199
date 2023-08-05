"""Provide utilities to manage recorded keeping for the pipeline"""

from typing import Optional, Tuple

import logging
from pathlib import Path

import mysql.connector


class PipelineDB:
    """
    The class manages record keeping for the pipeline.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self, user: str, password: str, database: str, host: str, port: int
    ):
        """
        Creates an instance of this class.

        Args:
            user: The user name with which to access the DB.
            password: The password with which to access the DB.
        """
        self.__connection = mysql.connector.connect(
            user=user,
            password=password,
            database=database,
            host=host,
            port=port,
        )
        self.__cursor = None

    def __bundle_key(self, name: str) -> Optional[int]:
        """
        Returns the bundle key, if any, for the supplied bundle name.
        """
        query = "select bundleKey from SaltedBundle where name = %s;"
        if None is self.__cursor:
            raise ValueError("There is no database transaction in progress")
        self.__cursor.execute(query, (name,))
        bundle_key = self.__cursor.fetchone()
        if None is bundle_key:
            return None
        return bundle_key[0]

    def begin_transaction(self):
        """
        Begins a transaction with the DB.
        """
        if None is self.__cursor:
            self.__cursor = self.__connection.cursor(buffered=True)

    def bundle_entry(  # pylint: disable=too-many-arguments
        self, bundle: str, path: str, data_name: str, metadata_name: str, done_name: str
    ) -> bool:
        """
        Records the entry of a bundle into the pipeline.

        Args:
            bundle: The name of the bundle entering.
            path: The path to the data file of the bundle in the "parking garage".
            data_name: The name of the data file in a receiving directory.
            metadata_name: The name of the metadata file in the"parking garage".
            done_name: The name of the metadata file in the"parking garage".

        Returns:
            True if the bundle is accepted into the pipeline.
        """
        if None is self.__cursor:
            raise ValueError("There is no database transaction in progress")
        logging.debug('bundle "%s" is entering the pipeline', bundle)
        bundle_key = self.__bundle_key(bundle)
        if None is bundle_key:
            query = "insert into SaltedBundle (name) values(%s);"
            self.__cursor.execute(query, (bundle,))
            bundle_key = self.__bundle_key(bundle)
        else:
            query = (
                "update Passage set whenAbandoned = CURRENT_TIMESTAMP() where bundle_bundleKey = "
                + "%s and whenExited is NULL;"
            )
            self.__cursor.execute(
                query,
                (bundle_key,),
            )
        query = (
            "insert into Passage (bundle_bundleKey, parkedPath, dataname, metadataName, doneName, "
            + "whenEntered) values(%s, %s, %s, %s, %s, CURRENT_TIMESTAMP());"
        )
        self.__cursor.execute(
            query,
            (
                bundle_key,
                path,
                data_name,
                metadata_name,
                done_name,
            ),
        )
        self.__connection.commit()
        return True

    def bundle_exit(
        self, bundle: str, entry_checksum: Optional[int], exit_checksum: int
    ) -> None:
        """
        Records the exit of a bundle from the pipeline.

        Args:
            bundle: The name of the bundle exiting.
            checksum: The current checksum of the bundle.
        """
        if None is self.__cursor:
            raise ValueError("The Database connection has been closed")
        bundle_key = self.__bundle_key(bundle)
        if None is bundle_key:
            raise ValueError(
                f'Bundle "{bundle}" has not enter the pipline, so can not exit'
            )
        query = (
            "update Passage set entryChecksum = %s, exitChecksum = %s, "
            + "whenExited = CURRENT_TIMESTAMP() where bundle_bundleKey = %s "
            + "and whenExited is null;"
        )
        self.__cursor.execute(
            query,
            (
                entry_checksum,
                exit_checksum,
                bundle_key,
            ),
        )
        self.__connection.commit()
        logging.debug('bundle "%s" has exited the pipeline', bundle)

    def close(self):
        """
        Closes any connections this object has opened.
        """
        self.end_transaction()
        if None is not self.__connection:
            self.__connection.close()
        self.__connection = None

    def end_transaction(self):
        """
        Begins a transaction with the DB.
        """
        if None is not self.__cursor:
            self.__cursor.close()
        self.__cursor = None

    def entry_checksum(self, bundle: str, exit_checksum: int) -> Optional[int]:
        """
        Returns the checksum that matches the supplied bundle and checksum.
        """
        if None is self.__cursor:
            raise ValueError("The Database connection has been closed")
        query = (
            "select entryChecksum from Passage join SaltedBundle on "
            + "(bundle_bundleKey = bundleKey) where name = %s and exitChecksum = %s "
            + "order by whenEntered desc;"
        )
        self.__cursor.execute(
            query,
            (
                bundle,
                exit_checksum,
            ),
        )
        result = self.__cursor.fetchone()
        if None is result:
            return None
        return result[0]

    def parked_paths(self, bundle: str) -> Tuple[Path, Path, Path, Path]:
        """
        Returns the of the bundle in the "parking garage"

        Args:
            bundle: The name of the bundle whose canonical path should be
                    returned.
        """
        if None is self.__cursor:
            raise ValueError("The Database connection has been closed")
        query = (
            "select parkedPath, dataName, metadataName, doneName from Passage join SaltedBundle on "
            + "(bundle_bundleKey = bundleKey) where name = %s "
            + "order by whenEntered desc;"
        )
        self.__cursor.execute(query, (bundle,))
        result = self.__cursor.fetchone()
        if None is result:
            raise ValueError('Bundle "{bundle}" does not have path information')
        bundle_data = Path(result[0])
        return (
            bundle_data,
            bundle_data.with_name(result[2]),
            bundle_data.with_name(result[3]),
            Path(result[1]),
        )
