"""" Library to deal with rpm operations.

I'm not going to implement every possible rpm operation. For rpm sign is needed.

Remember to install python3-rpm system package! without it this is not going to work.
"""""
import pexpect


class SigningError(Exception):
    def __init__(self, error_message: str):
        self.message = error_message

    def __str__(self):
        return f"I've found next error trying to sign file: {self.message}"


class UnsignedFileError(Exception):
    def __init__(self, file:str):
        self.file = file

    def __str__(self):
        return f"File {self.file} is not signed."


class PublicKeyImportError(Exception):
    def __init__(self, error_message: str):
        self.message = error_message

    def __str__(self):
        return f"Public key could not be imported in RPM database: {self.message}"


class PublicKeyNotFoundError(Exception):
    def __init__(self, fingerprint: str):
        self.fingerprint = fingerprint

    def __str__(self):
        return f"I could not find in RPM database a public key like this: {self.fingerprint}"


def import_public_key(key_file: str) -> None:
    """ Import public key as a trusted one for RPM packages.

    :param key_file: Public key file pathname to import.
    """
    child = pexpect.spawn(f"rpm --import {key_file}")
    # Wait until programs returns
    child.expect(pexpect.EOF)
    if child.exitstatus != 0:
        raise PublicKeyImportError(child.before)


def remove_public_key(fingerprint: str) -> None:
    """ Remove a public certificate from RPM database.

    :param fingerprint: GPG fingerprint of the public key to remove.
    """
    short_fingerprint = fingerprint[-8:]
    child = pexpect.spawn(f"rpm -qa gpg-pubkey*")
    child.expect(pexpect.EOF)
    rpm_key_list_text = child.before

    rpm_keys = rpm_key_list_text.split("\n")
    for key in rpm_keys:
        if short_fingerprint in key:
            child = pexpect.spawn(f"rpm -e {key}")
            child.expect(pexpect.EOF)
            return
    raise PublicKeyNotFoundError(fingerprint)


def sign(name: str, passphrase: str, file: str) -> None:
    """ Sign RPM package.

    :param name: Name (usually an email) to use as signer.
    :param passphrase: Passphrase for this private key.
    :param file: RPM file to sign.
    :raise myrpm.SigningError: If signing command meets an error this exception is raised with error string at its message field.
    :return: None
    """
    # child = pexpect.spawn(f"rpm --define {name} --addsign {file}")
    # child.pexpect("Passphrase: ")
    # child.sendline(passphrase)
    # # Wait until programs returns
    # child.expect(pexpect.EOF)
    # if child.exitstatus != 0:
    #     raise SigningError(child.before)
    raise NotImplementedError


def is_valid_signature(file: str) -> bool:
    """ Check whether this file is properly signed.

    :param file: File to check.
    :raise myrpm.UnsignedFileError: If current file is actually not signed at all.
    :return: True if it is well signed. False if signature is not correct.
    """
    # child = pexpect.spawn(f"rpm --checksig {file}")
    # # Wait until programs returns
    # child.expect(pexpect.EOF)
    # if "SIGNATURES NOT OK" in child.before:
    #     return False
    # elif "signatures" in child.before:
    #     return True
    # else:
    #     raise UnsignedFileError(file)
    raise NotImplementedError
