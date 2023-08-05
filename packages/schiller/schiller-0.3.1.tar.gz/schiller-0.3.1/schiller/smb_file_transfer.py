"""Test script for testing SMB."""
import os
import socket
from pathlib import Path
from typing import Optional, Any, List

from smb.SMBConnection import SMBConnection
from smb.smb_structs import OperationFailure


class SMBFileTransfer:
    """SMB wrapper for file transfer to and from remote FS.

    Implements the context manager interface.
    """

    conn: SMBConnection
    service_name: str

    def __init__(
        self, username: str, pw: str, server_name: str, domain: str, service_name: str
    ) -> None:
        """Constructor.

        Initializes SMB connection to remote File System.
        """

        self.service_name = service_name

        client_machine_name = socket.gethostname()
        server_ip = socket.gethostbyname(server_name)

        # Establish connection
        self.conn = SMBConnection(
            username,
            pw,
            client_machine_name,
            server_name,
            use_ntlm_v2=False,
            domain=domain,
        )
        connected = self.conn.connect(server_ip, 139)
        if not connected:
            raise ConnectionError("SMB connection could not be established.")
        pass

    def __enter__(self) -> "SMBFileTransfer":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.conn.close()

    def retrieve_file(self, dst_path_local: str, src_path_server: str) -> None:
        """Copies file from remote FS to local machine.

        Args:
            dst_path_local: Path of file to write.
            src_path_server: Path to file on remote FS.
        """
        with open(dst_path_local, "wb") as f:
            self.conn.retrieveFile(self.service_name, src_path_server, f)

    def store_file(self, dst_path_server: str, src_path_local: str) -> None:
        """Copies file from local machine to remote FS.

        Args:
            dst_path_server: Path of file to write.
            src_path_local: Path to local file to copy.
        """
        with open(src_path_local, "rb") as f:
            self.conn.storeFile(self.service_name, dst_path_server, f)

    def store_dir(self, dir_path_server: str, dir_path_local: str) -> None:
        """Transfers a directory recursively."""
        self.create_dir(dir_path_server, allow_exist=True)
        for f in os.listdir(dir_path_local):
            f_full = os.path.join(dir_path_local, f)
            f_dst_full = os.path.join(dir_path_server, f)
            if os.path.isdir(f_full):
                self.store_dir(f_dst_full, f_full)
            else:
                self.store_file(f_dst_full, f_full)
        pass

    def directory_exists(self, dir_path: str) -> bool:
        """Checks if a directory exists."""
        try:
            self.conn.getAttributes(self.service_name, dir_path)
            return True
        except OperationFailure:
            return False

    def create_dir(self, dir_path: str, allow_exist: bool = True) -> None:
        """Creates a directory on the remote FS.

        Args:
            dir_path: The path to the directory to create.
            allow_exist: If True, will not raise an exception if directory exists.
        """
        if allow_exist and self.directory_exists(dir_path):
            return

        self.conn.createDirectory(self.service_name, dir_path)

    def create_directories(
        self, base_dir_path: str, *dir_list: str, allow_exist: bool = True
    ) -> None:
        """Creates nested directory on the remote FS.

        `base_dir_path` is assumed to be an existing directory.

        Args:
            base_dir_path: The path to the base directory.
            *dir_list: Nested directories that will be created.
            allow_exist: If True, will not raise an exception if a directory exists.
        """
        attributes = self.conn.getAttributes(self.service_name, base_dir_path)
        assert attributes.isDirectory

        curr_dir = base_dir_path
        for d in dir_list:
            curr_dir = os.path.join(curr_dir, d)
            self.create_dir(curr_dir, allow_exist)

    def delete_dir(self, dir_path: str, recursively: bool = True) -> None:
        """Deletes a directory on the remote FS.

        Args:
            dir_path: The path to the directory to delete.
            recursively: Whether to delete the folder recursively.
        """
        if recursively:
            self.conn.deleteFiles(self.service_name, f"{dir_path}/*", True)
        self.conn.deleteDirectory(self.service_name, dir_path)

    def retrieve_dir_recursively(
        self,
        dst_dir: Path,
        src_dir: str,
        overwrite_files: bool = True,
        ext_list: Optional[List[str]] = None,
    ) -> None:
        """Retrieves a directory.

        Copies the content of directory `src_dir` on SFS
        into the local directory `dst_dir`. Folders are copied
        recursively and merged if they already exist.

        Args:
            dst_dir: Local destination directory.
            src_dir: Server source directory.
            overwrite_files: If true, already existing files will be overwritten.
            ext_list: List with file extensions that should be retrieved.
        """
        attributes = self.conn.getAttributes(
            self.service_name,
            src_dir,
        )
        assert attributes.isDirectory
        assert dst_dir.is_dir(), f"Directory {dst_dir} does not exist!"
        if ext_list is None:
            ext_list = []

        self._retrieve_dir_recursively(dst_dir, src_dir, ext_list, overwrite_files)

    def _retrieve_dir_recursively(
        self,
        dst_dir: Path,
        src_dir: str,
        ext_list: List[str],
        overwrite_files: bool = True,
    ) -> None:
        """Recursive helper function for :func:`retrieve_dir_recursively`."""
        file_list = self.conn.listPath(self.service_name, src_dir)
        for f in file_list:
            f_name = f.filename
            if f_name in [".", ".."]:
                continue

            full_path_src = os.path.join(src_dir, f_name)
            full_path_dst = dst_dir / f_name

            # Apply recursion
            if f.isDirectory:
                full_path_dst.mkdir(exist_ok=True, parents=True)
                self._retrieve_dir_recursively(
                    full_path_dst, full_path_src, ext_list, overwrite_files
                )
            else:
                if not self._valid_extension(f_name, ext_list):
                    continue
                if not full_path_dst.is_file() or overwrite_files:
                    self.retrieve_file(full_path_dst, full_path_src)

        pass

    @staticmethod
    def _valid_extension(f_name: str, ext_list: List) -> bool:
        return len(ext_list) == 0 or any([f_name.endswith(e) for e in ext_list])

    pass
