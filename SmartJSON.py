##############################################
# SmartJSON
##############################################
### > Designed for MyWinterSaveSlots
##############################################
### > Have fun with dissecting what I made.
##############################################

import json
from random import randint as rnd
from enum import Enum as _enum
import os


class Enum:
    class DataType(_enum):
        Serialized = 1
        Deserialized = 2
        Unknown = 3


class SmartJSON:
    def __init__(self, HookedFilePath: any, UseColorPlus: bool = False, LogIntoConsole: bool = True) -> None:  # type: ignore
        """
        Docstring for __init__

        :param self: Reference to obj
        :param HookedFilePath: Initial file to hook onto. Leave empty if you will change it later with ChangeHookedFile()
        :type HookedFilePath: any
        :param UseColorPlus: Whether to use the Color+ library. False by default. Requires the existence of the Color+ dependency.
        :type UseColorPlus: bool
        :param LogIntoConsole: Whether to log startup errors into console - does not affect function-specific error logging.
        :type LogIntoConsole: bool
        """

        self.LogIntoConsole = LogIntoConsole
        print("Initializing SmartJSON...")
        self.UseColorPlus = UseColorPlus
        self.Lock = False
        self.State = "Initializing"

        if self.UseColorPlus:
            try:
                import ColorPlus
            except ModuleNotFoundError:
                self.UseColorPlus = False
                self.clog("ColorPlus was not found! Continuing without colors.", "Error")

        self.AttachedFileAbsPath = None

        if self.UseColorPlus:
            try:
                import ColorPlus
            except ModuleNotFoundError:
                self.clog("Atleast one or more modules are missing! (ColorPlus)", "Error")
                self.clog("SmartJSON cannot continue without ColorPlus. Exiting now.", "Error")
                exit()

        if type(HookedFilePath) is type(str):
            self.clog("Attempting to hook onto file...")
            self.HookedFileExists = False

            try:
                with open(str(HookedFilePath), "r") as f:
                    self.AttachedFileAbsPath = os.path.abspath(str(HookedFilePath))
            except FileNotFoundError:
                self.clog("Given JSON file path does not exist. Continuing in unhooked state.", "Error")
                self.State = "AwaitHook"
            else:
                self.clog("File found!")
                self.clog(f"Attached to file at {self.AttachedFileAbsPath}")
                self.State = "Initialized"
        else:
            self.clog(
                "No request for immediate file hook, continuing in unhooked mode. (Cannot interact until ChangeHookedFile() is called!)",
                "Warning",
            )
            self.State = "AwaitHook"

    def GetValue(self, Key: str, LogErrors: bool = True) -> tuple[bool, bool, any]:  # type: ignore
        if self.State == "Initialized":
            DataFromFile = None

            try:
                with open(str(self.AttachedFileAbsPath), "r") as f:
                    DataFromFile = f.read()
            except FileNotFoundError:
                return False, False, None
            else:
                OK, DeserializedData = self.Deserialize(DataFromFile, True)

                if not OK:
                    if LogErrors:
                        self.clog("Failed with deserialization in GetValue()!", "Error")
                    return False, False, None

                FoundVal = None

                try:
                    FoundVal = DeserializedData[Key]  # type: ignore
                except (KeyError, IndexError):
                    return False, False, None
                else:
                    IsNil = FoundVal == None
                    return True, IsNil, FoundVal
        else:
            if LogErrors:
                self.clog("Attempted to call a function that is restricted when unhooked!", "Warning")
            return False, False, None

    def HookOntoFile(self, AbsolutePath: str, LogError: bool = True, CreateIfNotExists: bool = False) -> bool:
        if self.State == "AwaitHook":
            try:
                with open(AbsolutePath, "r") as f:
                    pass
            except FileNotFoundError:
                if LogError and not CreateIfNotExists:
                    self.clog(
                        "Attempted to hook onto file, but this file wasn't found! Resuming in unhooked state.",
                        "Warning",
                    )
                    return False
                elif LogError and CreateIfNotExists:
                    self.clog(
                        "Attempted to hook onto file, but it wasn't found. Will create and call self again.",
                        "Warning"
                    )
                    with open(AbsolutePath, "w") as f2:
                        f2.write("{}")
                    return self.HookOntoFile(AbsolutePath=AbsolutePath, LogError=True, CreateIfNotExists=False)
            else:
                self.AttachedFileAbsPath = AbsolutePath
                self.State = "Initialized"
                return True
        else:
            if LogError:
                self.clog("Already hooked to a file!", "Warning")
            return False

    def Unhook(self, LogError: bool) -> bool:
        if self.State == "Initialized":
            self.AttachedFileAbsPath = None
            self.State = "AwaitHook"
            return True
        else:
            if LogError:
                self.clog(
                    "Attempted to unhook even when it's already unhooked or still initializing!",
                    "Warning",
                )
            return False

    def LoadEntireFile(
        self, ReturnType: Enum.DataType = Enum.DataType.Serialized, LogError: bool = True
    ) -> tuple[bool, object]:  # type: ignore
        if self.State == "Initialized":
            FileData = None

            try:
                with open(str(self.AttachedFileAbsPath), "r") as f:
                    FileData = f.read()
            except FileNotFoundError:
                if LogError:
                    self.clog(
                        "Attempted to read all data from attached file, failed because it doesn't exist!",
                        "Error",
                    )
                return False, None
            else:
                if FileData != "" and FileData != None:
                    if ReturnType == Enum.DataType.Serialized:
                        return True, FileData
                    elif ReturnType == Enum.DataType.Deserialized:
                        Deserialized = None

                        try:
                            OK, Deserialized = self.Deserialize(FileData, False)
                            if not OK:
                                raise TypeError("Failed to deserialize!")
                        except (json.JSONDecodeError, TypeError):
                            if LogError:
                                self.clog(
                                    "Error when attempting to deserialize data per request. Check the JSON syntax.",
                                    "Error",
                                )
                            return False, None
                        else:
                            return True, Deserialized
        else:
            if LogError:
                self.clog("Attempted to call a function that is restricted when unhooked!", "Warning")
            return False, None
        




        def SetEntireFile(self, Data: object, LogError: bool = True) -> bool:
            if self.State == "Initialized":

                # Ensure data is deserialized (basically: not a JSON string)
                if isinstance(Data, str):
                    if LogError:
                        self.clog("SetEntireFile expects DESERIALIZED data, not serialized JSON string.", "Error")
                    return False

                OK, Serialized = self.Serialize(Data, True)

                if not OK:
                    if LogError:
                        self.clog("Failed to serialize data in SetEntireFile!", "Error")
                    return False

                NameOfTemp = f"temp-{rnd(100000, 999999)}"

                try:
                    with open(NameOfTemp, "w+") as f:
                        f.write(Serialized)
                except Exception:
                    if LogError:
                        self.clog(
                            "Failed to save to temporary file. Backing off from touching the hooked json file.",
                            "Error",
                        )
                    return False

                try:
                    with open(str(self.AttachedFileAbsPath), "w") as f:
                        f.write(Serialized)
                except (IOError, OSError):
                    if LogError:
                        self.clog(
                            "Failed to save serialized data to file in SetEntireFile. File may be corrupt.",
                            "Error",
                        )
                    return False
                else:
                    return True
                finally:
                    os.remove(NameOfTemp)

            else:
                if LogError:
                    self.clog("Attempted to call a function that is restricted when unhooked!", "Warning")
                return False


    

    def SetValueOfKey(self, Key: str, Value: any, LogError: bool = True) -> bool:  # type: ignore
        if self.State == "Initialized":
            OK, Data = self.LoadEntireFile(Enum.DataType.Deserialized, True)

            if OK and Data:
                X = Data

                try:
                    if isinstance(X, dict):
                        _m = X[Key]
                        X[Key] = Value
                    else:
                        setattr(X, Key, Value)
                except Exception:
                    if LogError:
                        self.clog(
                            "Key not found when attempted to set value of key. Changes not applied.",
                            "Error",
                        )
                    return False
                else:
                    OK2, Y = self.Serialize(X, True)

                    if not OK2:
                        if LogError:
                            self.clog("Failed to serialize in SetValueOfKey", "Error")
                        return False

                    NameOfTemp = f"temp-{rnd(100000, 999999)}"

                    try:
                        with open(NameOfTemp, "w+") as f:
                            f.write(Y)
                    except Exception:
                        if LogError:
                            self.clog(
                                "Failed to save to temporary file. Backing off from touching the hooked json file.",
                                "Error",
                            )
                        return False

                    try:
                        with open(str(self.AttachedFileAbsPath), "w") as f:
                            f.write(Y)
                    except (IOError, OSError):
                        if LogError:
                            self.clog(
                                "Failed to save serialized data to file in SetValueOfKey. File may be corrupt.",
                                "Error",
                            )
                        return False
                    else:
                        return True
                    finally:
                        os.remove(NameOfTemp)
        else:
            if LogError:
                self.clog("Attempted to call a function that is restricted when unhooked!", "Warning")
            return False

    def Serialize(self, UnserializedData: object, LogError: bool = True) -> tuple[bool, str]:
        x = ""
        try:
            x = json.dumps(UnserializedData)
        except Exception:
            if LogError:
                self.clog(
                    "The JSON library errored when parsing this dictionary. Check your Python dict.",
                    "Error",
                )
            return False, x
        else:
            return True, x

    def Deserialize(self, SerializedData: str, LogError: bool = True) -> tuple[bool, dict]:
        x = SerializedData

        try:
            x = json.loads(x)
        except json.JSONDecodeError:
            if LogError:
                self.clog("JSON decode error! Check your JSON syntax!", "Error")
            return False, {}
        except Exception:
            if LogError:
                self.clog(
                    "Generic error with deserializing! Is your JSON syntax correct?",
                    "Error",
                )
            return False, {}
        else:
            return True, x

    def clog(self, Text: str, Severity: str = "Info") -> None:
        if (
            not self.State == "Initializing"
            and not self.State == "Initialized"
            and not self.State == "AwaitHook"
        ):
            print("[clog] Error: Main module SmartJSON not initialized!")
            return

        if not self.LogIntoConsole:
            return

        if self.UseColorPlus:
            import ColorPlus

            if Severity.lower() == "error":
                Severity = ColorPlus.ColorPlus.Red + Severity
                Text = Text + ColorPlus.ColorPlus.Reset
            elif Severity.lower().startswith("warn"):
                Severity = ColorPlus.ColorPlus.Yellow + Severity
                Text = Text + ColorPlus.ColorPlus.Reset
            elif Severity.lower().startswith("info"):
                Severity = ColorPlus.ColorPlus.Blue + Severity
                Text = Text + ColorPlus.ColorPlus.Reset

            print(
                f"{ColorPlus.ColorPlus.BrightMagenta}[SMARTJSON]{ColorPlus.ColorPlus.Reset} {Severity}: {Text}"
            )
        else:
            print(f"[SMARTJSON] {Severity}: {Text}")


print("Loaded SmartJSON - created by JustDingusToo on NexusMods.")

if __name__ == "__main__":
    print(
        """
0=0=0=0=0=0=0=0=0=0=0=0=0=0=0=0=0=0=0=0=0=0=0=0
You have run SmartJSON directly.
A test initialization will now happen.
0=0=0=0=0=0=0=0=0=0=0=0=0=0=0=0=0=0=0=0=0=0=0=0
"""
    )

    x = SmartJSON("settings.json", True)
    y = x.SetValueOfKey("x", "x")
