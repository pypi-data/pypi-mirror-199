import hashlib
import json
import logging
import os
import SimpleWorkspace as sw
from SimpleWorkspace.IO.File import FileInfo
import unittest
import time
from SimpleWorkspace.SettingsProviders import SettingsManager_AutoMapped_JSON, SettingsManager_JSON, SettingsManager_BasicConfig
from SimpleWorkspace.Utility.StopWatch import StopWatch
from configparser import ConfigParser 
import gzip

class BaseTestCase(unittest.TestCase):
    testAppName = "SimpleWorkspaceTesting"
    testAppCompany = "TestLabFacility"
    testPath = "./out"
    controlFile = "c27182b2-af7b-5398-b262-8517732a9b53.controlfile"

    def setUp(self) -> None:
        sw.IO.Directory.Create(self.testPath)
        sw.IO.File.Create(f"{self.testPath}/{self.controlFile}")
        
    def tearDown(self) -> None:
        logging.shutdown()
        if not (os.path.exists(f"{self.testPath}/{self.controlFile}")):
            raise Exception("Control file missing! not removing contents for safety reasons...")
        sw.IO.Directory.Remove(self.testPath)

        
    @classmethod
    def setUpClass(self):
        pass

    @classmethod
    def tearDownClass(self) -> None:
        pass


class ConversionTest(BaseTestCase):
    def test_Times_HasCorrectSeconds(self):
        assert sw.Enums.TimeEnum.Day.value * 2 ==  172800
        assert sw.Enums.TimeEnum.Hour.value * 2 ==  7200
        assert sw.Enums.TimeEnum.Minute.value * 2 ==  120


class IO_FileTests(BaseTestCase):
    testPath_Samples = BaseTestCase.testPath + "/FileSamples"
    testPath_Samples_byteTestFile = testPath_Samples + "/byteTestFile.bin"
    testPath_Samples_byteTestFile_content = b""
    testPath_Samples_textTestFile = testPath_Samples + "/textTestFile.txt"
    testPath_Samples_textTestFile_content = "1234567890"
    testPath_Samples_nestedFolder = testPath_Samples + "/nestedTest"
    testPath_Samples_nestedFolder_folderCount = 15
    testPath_Samples_nestedFolder_textFileCount = 6
    testPath_Samples_nestedFolder_binaryFileCount = 5
    testPath_Samples_nestedFolder_allFileCount = testPath_Samples_nestedFolder_textFileCount + testPath_Samples_nestedFolder_binaryFileCount
    testPath_Samples_nestedFolder_entryCount = testPath_Samples_nestedFolder_folderCount + testPath_Samples_nestedFolder_allFileCount
    testPath_Samples_nestedFolder_fileContentText = "1234567890"
    testPath_Samples_nestedFolder_fileContentBin = b"12\x004567890"
    testPath_Samples_nestedFolder_totalFileSize = testPath_Samples_nestedFolder_allFileCount * len(testPath_Samples_nestedFolder_fileContentText)

    def GenerateSampleFiles(self):
        sw.IO.Directory.Create(self.testPath_Samples)
        sw.IO.Directory.Create(self.testPath_Samples_nestedFolder + "/tree1/sub1/sub2/sub3")
        sw.IO.Directory.Create(self.testPath_Samples_nestedFolder + "/tree1/sub1/splitsub2/sub3")
        sw.IO.Directory.Create(self.testPath_Samples_nestedFolder + "/tree2/sub1/sub2/sub3")
        sw.IO.Directory.Create(self.testPath_Samples_nestedFolder + "/tree3/sub1/sub2/sub3")
        sw.IO.Directory.Create(self.testPath_Samples_nestedFolder + "/tree3/sub1/sub2/splitsub3")
        sw.IO.File.Create(self.testPath_Samples_nestedFolder + "/tree1/sub1/splitsub2/sub3/sample1.txt", self.testPath_Samples_nestedFolder_fileContentText)
        sw.IO.File.Create(self.testPath_Samples_nestedFolder + "/tree1/sub1/sub2/sub3/sample1.txt", self.testPath_Samples_nestedFolder_fileContentText)
        sw.IO.File.Create(self.testPath_Samples_nestedFolder + "/tree1/sub1/sub2/sample1.txt", self.testPath_Samples_nestedFolder_fileContentText)
        sw.IO.File.Create(self.testPath_Samples_nestedFolder + "/tree1/sub1/sample1.txt", self.testPath_Samples_nestedFolder_fileContentText)
        sw.IO.File.Create(self.testPath_Samples_nestedFolder + "/tree1/sample1.txt", self.testPath_Samples_nestedFolder_fileContentText)
        sw.IO.File.Create(self.testPath_Samples_nestedFolder + "/tree2/sub1/sub2/sub3/sample1.txt", self.testPath_Samples_nestedFolder_fileContentText)
        sw.IO.File.Create(self.testPath_Samples_nestedFolder + "/tree3/sub1/sub2/splitsub3/sample1.bin", self.testPath_Samples_nestedFolder_fileContentBin)
        sw.IO.File.Create(self.testPath_Samples_nestedFolder + "/tree3/sub1/sub2/sub3/sample1.bin", self.testPath_Samples_nestedFolder_fileContentBin)
        sw.IO.File.Create(self.testPath_Samples_nestedFolder + "/tree3/sub1/sub2/sample1.bin", self.testPath_Samples_nestedFolder_fileContentBin)
        sw.IO.File.Create(self.testPath_Samples_nestedFolder + "/tree3/sub1/sample1.bin", self.testPath_Samples_nestedFolder_fileContentBin)
        sw.IO.File.Create(self.testPath_Samples_nestedFolder + "/tree3/sample1.bin", self.testPath_Samples_nestedFolder_fileContentBin)

        sw.IO.File.Create(self.testPath_Samples_textTestFile, self.testPath_Samples_textTestFile_content)
        for i in range(255):
            self.testPath_Samples_byteTestFile_content += bytes(chr(i), "utf-8")
        for i in range(255):
            self.testPath_Samples_byteTestFile_content += bytes(chr(i), "utf-8")
        sw.IO.File.Create(self.testPath_Samples_byteTestFile, self.testPath_Samples_byteTestFile_content)


    def setUp(self) -> None:
        super().setUp()
        self.GenerateSampleFiles()

    def test_FileContainer_GetsValidPaths(self):
        t0 = FileInfo("a/b/c.exe")
        t1 = FileInfo("a/b/c")
        t2 = FileInfo("a/b/.exe")
        t3 = FileInfo(".exe")
        t4 = FileInfo("c")
        t5 = FileInfo("c.exe")
        t6 = FileInfo(".")
        t7 = FileInfo("a.,-.asd/\\/b.,ca.asd/c.,..exe")

        assert (t0.fileExtension == ".exe" and t0.filename == "c" and t0.tail == "a/b/" and t0.head == "c.exe")
        assert (t1.fileExtension == "" and t1.filename == "c" and t1.tail == "a/b/" and t1.head == "c")
        assert (t2.fileExtension == ".exe" and t2.filename == "" and t2.tail == "a/b/" and t2.head == ".exe")
        assert (t3.fileExtension == ".exe" and t3.filename == "" and t3.tail == "" and t3.head == ".exe")
        assert (t4.fileExtension == "" and t4.filename == "c" and t4.tail == "" and t4.head == "c")
        assert (t5.fileExtension == ".exe" and t5.filename == "c" and t5.tail == "" and t5.head == "c.exe")
        assert (t6.fileExtension == "." and t6.filename == "" and t6.tail == "" and t6.head == ".")
        assert (t7.fileExtension == ".exe" and t7.filename == "c.,." and t7.tail == "a.,-.asd/\\/b.,ca.asd/" and t7.head == "c.,..exe")

    def test_File_ReadsCorrectTypes(self):
        data = sw.IO.File.Read(self.testPath_Samples_byteTestFile)
        assert (type(data) is str)
        data = sw.IO.File.Read(self.testPath_Samples_byteTestFile, callback=lambda x: self.assertEqual(type(x), str))
        assert data is None

        ##bytes##
        data = sw.IO.File.Read(self.testPath_Samples_byteTestFile, getBytes=True)
        assert type(data) is bytes
        data = sw.IO.File.Read(self.testPath_Samples_byteTestFile, callback=lambda x: self.assertEqual(type(x), bytes), getBytes=True)
        assert data is None

    def test_Hash_GetsCorrectHash(self):
        originalHash = sw.IO.File.Hash(self.testPath_Samples_byteTestFile, hashFunc=hashlib.sha256())

        #
        sha256 = hashlib.sha256()
        sha256.update(self.testPath_Samples_byteTestFile_content)
        resultHash = sha256.hexdigest()
        assert originalHash ==  resultHash
        #
        sha256 = hashlib.sha256()
        sw.IO.File.Read(self.testPath_Samples_byteTestFile, callback=sha256.update, getBytes=True)
        resultHash = sha256.hexdigest()
        assert originalHash ==  resultHash
        #
        sha256 = hashlib.sha256()
        sw.IO.File.Read(self.testPath_Samples_byteTestFile, callback=sha256.update, readSize=100, getBytes=True)
        resultHash = sha256.hexdigest()
        assert originalHash ==  resultHash
        #
        sha256 = hashlib.sha256()
        sw.IO.File.Read(self.testPath_Samples_byteTestFile, callback=sha256.update, readLimit=len(self.testPath_Samples_byteTestFile_content), getBytes=True)
        resultHash = sha256.hexdigest()
        assert originalHash ==  resultHash

    def test_File_Reading_ReadsCorrect(self):
        data = sw.IO.File.Read(self.testPath_Samples_textTestFile, readLimit=10, getBytes=False)
        assert data ==  self.testPath_Samples_textTestFile_content

        #
        tmpList = []
        sw.IO.File.Read(self.testPath_Samples_byteTestFile, callback=tmpList.append, readSize=50, readLimit=200, getBytes=True)
        assert (len(tmpList) == 4) and (len(tmpList[0]) == 50)

        #
        tmpList = []
        sw.IO.File.Read(self.testPath_Samples_byteTestFile, callback=lambda x: tmpList.append(x), readSize=50, getBytes=True)
        assert len(tmpList[0]) ==  50

        #
        tmpList = []
        sw.IO.File.Read(self.testPath_Samples_byteTestFile, callback=tmpList.append, readSize=50, readLimit=4, getBytes=True)
        assert (len(tmpList) == 1) and (len(tmpList[0]) == 4)

        #
        tmpList = []
        sw.IO.File.Read(self.testPath_Samples_byteTestFile, callback=tmpList.append, readSize=-1, readLimit=4, getBytes=True)
        assert len(tmpList[0]) ==  4

    def test_Directories_ListsAll(self):
        fileSizes = []
        sw.IO.Directory.List(self.testPath_Samples_nestedFolder, lambda x: fileSizes.append(os.path.getsize(x)), includeDirs=True)
        fileSize = 0
        for i in fileSizes:
            fileSize += i
        assert fileSize ==  self.testPath_Samples_nestedFolder_totalFileSize

        #
        tmpList = []
        sw.IO.Directory.List(self.testPath_Samples_nestedFolder, tmpList.append, includeDirs=False)
        assert len(tmpList) ==  self.testPath_Samples_nestedFolder_allFileCount

        #
        tmpList = []
        sw.IO.Directory.List(self.testPath_Samples_nestedFolder, tmpList.append, includeDirs=True)
        assert len(tmpList) ==  self.testPath_Samples_nestedFolder_entryCount

    def test_Directories_ListsOnlyDirectories(self):
        #
        tmpList = sw.IO.Directory.List(self.testPath_Samples_nestedFolder, includeDirs=False, includeFiles=False)
        assert len(tmpList) ==  0

        #
        tmpList = sw.IO.Directory.List(self.testPath_Samples_nestedFolder, includeDirs=True, includeFiles=False)
        assert len(tmpList) ==  self.testPath_Samples_nestedFolder_folderCount

    def test_Directories_ListsAll_maxDepth(self):

        #
        tmpList = []
        sw.IO.Directory.List(self.testPath_Samples_nestedFolder, tmpList.append, includeDirs=False, maxRecursionDepth=9999)
        assert len(tmpList) ==  self.testPath_Samples_nestedFolder_allFileCount

        totalFilesInLevel1 = len(os.listdir(self.testPath_Samples_nestedFolder))
        #
        tmpList = []
        sw.IO.Directory.List(self.testPath_Samples_nestedFolder, tmpList.append, includeDirs=True, maxRecursionDepth=1)
        assert len(tmpList) ==  totalFilesInLevel1

        totalFilesInLevel2 = totalFilesInLevel1
        for filename in os.listdir(self.testPath_Samples_nestedFolder):
            totalFilesInLevel2 += len(os.listdir(os.path.join(self.testPath_Samples_nestedFolder, filename)))

        sw.IO.Directory.List(self.testPath_Samples_nestedFolder, tmpList.append, includeDirs=True, maxRecursionDepth=2)
        assert len(tmpList) ==  totalFilesInLevel2

    def test_Directories_callbackFiltering_1(self):
        tmpList = []
        sw.IO.Directory.List(self.testPath_Samples_nestedFolder, tmpList.append, includeFilter = lambda x: x.endswith(".txt") or x.endswith(".exe"))
        totalTxt = 0
        totalExe = 0
        for i in tmpList:
            fcon = FileInfo(i)
            if fcon.fileExtension == ".exe":
                totalExe += 1
            if fcon.fileExtension == ".txt":
                totalTxt += 1
        assert totalTxt ==  self.testPath_Samples_nestedFolder_textFileCount
        assert totalExe ==  0

    def test_Directories_regexFiltering_1(self):
        tmpList = []
        sw.IO.Directory.List(self.testPath_Samples_nestedFolder, tmpList.append, includeFilter=r"/\.(exe|txt)/i")
        totalTxt = 0
        totalExe = 0
        for i in tmpList:
            fcon = FileInfo(i)
            if fcon.fileExtension == ".exe":
                totalExe += 1
            if fcon.fileExtension == ".txt":
                totalTxt += 1
        assert totalTxt ==  self.testPath_Samples_nestedFolder_textFileCount
        assert totalExe ==  0

    def test_Directories_regexFiltering_2(self):
        tmpList = []
        sw.IO.Directory.List(self.testPath_Samples_nestedFolder, tmpList.append, includeFilter=r"/\.(bin)$/i")
        for path in tmpList:
            assert sw.IO.File.Read(path, getBytes=True) ==  self.testPath_Samples_nestedFolder_fileContentBin
        assert len(tmpList) ==  self.testPath_Samples_nestedFolder_binaryFileCount

    def test_Directories_regexFiltering_3(self):
        tmpList = []
        sw.IO.Directory.List(self.testPath_Samples_nestedFolder, tmpList.append, includeFilter=r"\.(nonexisting)$")
        assert len(tmpList) ==  0

    def test_Directories_regexFiltering_AllFiles_1(self):
        tmpList = []
        sw.IO.Directory.List(self.testPath_Samples_nestedFolder, tmpList.append, includeFilter=r"\.(bin|txt)$")
        assert len(tmpList) ==  self.testPath_Samples_nestedFolder_allFileCount

    def test_Directories_regexFiltering_AllFiles_1(self):
        tmpList = []
        sw.IO.Directory.List(self.testPath_Samples_nestedFolder, tmpList.append, includeFilter=r"/.*/i")
        assert len(tmpList) ==  self.testPath_Samples_nestedFolder_entryCount


class UtilityTest(BaseTestCase):
    sampleText = "Hello person1 with short hair\n" "Hello person2 with shoes\n" "Hello person3 with jacket\n" "this is a new walkthrough of version 1.2.8.12 of this app\n" "older available versions are following: v1.2.8.11, v1.2.8.10, v1.2.5.1, v1.1.2.9,\n" "good luck\n"

    def test_Regex_replace_flag_MultiLine(self):
        res = sw.Utility.Regex.Replace(r"/^Hello person(.) /", r"Hello bobby0 ", self.sampleText)
        resReplaced = sw.Utility.Regex.Match(r"/bobby. /i", res)
        assert len(resReplaced) ==  3
        assert resReplaced[0][0] ==  "bobby0 "

        res = sw.Utility.Regex.Replace(r"/person(.) /", r"bobby\1 ", self.sampleText)
        resReplaced = sw.Utility.Regex.Match(r"/bobby. /i", res)
        assert len(resReplaced) ==  3
        assert resReplaced[0][0] ==  "bobby1 "
        assert resReplaced[1][0] ==  "bobby2 "

        result = sw.Utility.Regex.Replace(r"/hej (.*?) /i", r"bye \1 or \g<1> ", "hej v1.0 hej v2.2 hejsan v3.3")  # result = "bye v1.0 or v1.0 bye v2.2 or v2.2 hejsan v3.3"
        assert result ==  "bye v1.0 or v1.0 bye v2.2 or v2.2 hejsan v3.3"

    def test_Regex_replace_flag_DotAll(self):
        res = sw.Utility.Regex.Replace(r"/^Hello person(.) /s", r"bobby0 ", self.sampleText)
        resReplaced = sw.Utility.Regex.Match(r"/bobby. /i", res)
        assert len(resReplaced) ==  1
        assert resReplaced[0][0] ==  "bobby0 "

    def test_Regex_Match_flag_MultiLine(self):
        res = sw.Utility.Regex.Match(r"/^Hello (person.*?) /", self.sampleText)
        assert res[0][0] ==  "Hello person1 "
        assert res[0][1] ==  "person1"

        assert res[1][0] ==  "Hello person2 "
        assert res[1][1] ==  "person2"

        assert res[2][0] ==  "Hello person3 "
        assert res[2][1] ==  "person3"
        assert len(res[0]) ==  2
        assert len(res) ==  3

    def test_Regex_Match_flag_DotAll(self):
        res = sw.Utility.Regex.Match(r"/^Hello (person.*?) /s", self.sampleText)
        assert res[0][0] ==  "Hello person1 "
        assert res[0][1] ==  "person1"
        assert len(res[0]) ==  2
        assert len(res) ==  1

        res = sw.Utility.Regex.Match(r"/^Hello.*(with) (jacket)/s", self.sampleText)
        assert res[0][0] ==  "Hello person1 with short hair\nHello person2 with shoes\nHello person3 with jacket"
        assert len(res[0]) ==  3
        assert len(res) ==  1

    def test_Regex_flag_CaseSensitivity(self):
        res = sw.Utility.Regex.Match(r"/hello person\d/", self.sampleText)
        assert res ==  None
        res = sw.Utility.Regex.Match(r"/Hello person\d/", self.sampleText)
        assert res[0][0] ==  "Hello person1"
        assert res[1][0] ==  "Hello person2"
        assert res[2][0] ==  "Hello person3"
        assert len(res[0]) ==  1
        assert len(res) ==  3


class AppTest(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        sw.App.Setup(self.testAppName, self.testAppCompany)

    def tearDown(self) -> None:
        super().tearDown()
        if self.testAppName in sw.App.path_currentAppData and self.testAppCompany in sw.App.path_currentAppData:
            sw.IO.Directory.Remove(sw.App.path_currentAppData)

    def test_settings_json(self):
        sw.App.settingsManager.LoadSettings()
        sw.App.settingsManager.Settings["test1"] = 10
        sw.App.settingsManager.Settings["test2"] = 20
        sw.App.settingsManager.SaveSettings()
        savedSettingData = sw.IO.File.Read(sw.App.settingsManager._settingsPath)
        obj = json.loads(savedSettingData)
        assert obj == {"test1": 10, "test2": 20}

    def test_appdata_logging(self):
        sw.App.logger.debug("test log 1")
        sw.App.logger.debug("test log 2")
        sw.App.logger.debug("test log 3")
        logData = sw.IO.File.Read(sw.App._loggerFilepath)
        result = sw.Utility.Regex.Match(f"/(.*?) (\w+?) <(.*?)>: (.*)/i", logData)
        assert len(result) ==  3
        assert result[0][4] ==  "test log 1"
        assert result[1][4] ==  "test log 2"
        assert result[2][4] ==  "test log 3"
        pass

class Utility_StopWatchTest(BaseTestCase):
    def AccurateSleepMS(self, ms):
        start = time.time()
        time.sleep(ms / 1000)
        elapsed = time.time() - start
        return elapsed * 1000

    def InDistance(self, val1, val2, maxDistance):
        distance = abs(val1 - val2)
        if distance > maxDistance:
            return False
        return True

    def test_HappyFlow(self):
        #we do indistance 5ms resolution, this means that just retrieving the time from stopwatch may take up to 5ms in theory
        stopWatch = StopWatch()

        res = stopWatch.GetElapsedMilliseconds()
        assert res == 0, f"should be 0 ms, got {res}"

        stopWatch.Start()
        actualSleepTime = self.AccurateSleepMS(1)

        res = stopWatch.GetElapsedMilliseconds()
        assert self.InDistance(res, actualSleepTime, 5), f"should be {actualSleepTime} ms, got {res}"

        # should do nothing since already running
        stopWatch.Start()
        stopWatch.Start()

        actualSleepTime += self.AccurateSleepMS(1)
        res = stopWatch.GetElapsedMilliseconds()
        assert self.InDistance(res, actualSleepTime, 5), f"should be {actualSleepTime} ms, got {res}"

        stopWatch.Stop()
        res = stopWatch.GetElapsedMilliseconds()
        assert self.InDistance(res, actualSleepTime, 5), f"should be {actualSleepTime} ms still, got {res}"

        self.AccurateSleepMS(1)  # skip this, since we just want to check if not counted after Stopped timer
        assert self.InDistance(res, actualSleepTime, 5), f"should be {actualSleepTime} ms still since we stopped after delay had passed, got {res}"

        stopWatch.Start()
        res = stopWatch.GetElapsedMilliseconds()
        assert self.InDistance(res, actualSleepTime, 5), f"should be {actualSleepTime} ms still since we started after delay had passed, got {res}"

        actualSleepTime += self.AccurateSleepMS(1)
        res = stopWatch.GetElapsedMilliseconds()
        assert self.InDistance(res, actualSleepTime, 5), f"should be {actualSleepTime} ms, got {res}"

        stopWatch.Start()
        stopWatch.Stop()
        stopWatch.Start()
        stopWatch.Stop()
        stopWatch.Start()
        stopWatch.Stop()
        res = stopWatch.GetElapsedMilliseconds()
        assert self.InDistance(res, actualSleepTime, 5), f"should be {actualSleepTime} ms still, got {res}"

        stopWatch.Reset()
        res = stopWatch.GetElapsedMilliseconds()
        assert res == 0, f"should be 0 ms since we resetted time, got {res}"
class Utility_RotatingLogFileReader(BaseTestCase):
    def CreateLog(self, logname = "tmp.log"):
        logPath = f"{self.testPath}/{logname}"
        sw.IO.File.Create(logPath, "1\n2\n3\n")
        return logPath
    
    def CreateLog_Delayed_NoCompressions(self):
        logpath = self.CreateLog()
        os.rename(logpath, logpath + ".1")
        sw.IO.File.Create(logpath, "4\n5\n6\n")
        return logpath
    
    def CreateLog_Delayed_WithCompressions(self):
        logpath = self.CreateLog_Delayed_NoCompressions()

        with open(f"{logpath}.1", 'rb') as f_in, gzip.open(f"{logpath}.2.gz", 'wb') as f_out:
            f_out.writelines(f_in)
        os.replace(f"{logpath}", f"{logpath}.1")
        sw.IO.File.Create(logpath, "7\n8\n9\n")
        return logpath
    
    def CreateLog_WithCompression(self):
        logpath = self.CreateLog()
        
        with open(f"{logpath}", 'rb') as f_in, gzip.open(f"{logpath}.1.gz", 'wb') as f_out:
            f_out.writelines(f_in)
        sw.IO.File.Create(logpath, "4\n5\n6\n")
        return logpath
    

    def test_SingleLogFile(self):
        logpath = self.CreateLog()
        self.assertEqual(
            sw.Utility.Log.RotatingLogReader(logpath).ToString(),
            "1\n2\n3\n"
        )

    def test_DelayedLog_withNoCompressedFiles(self):
        logpath = self.CreateLog_Delayed_NoCompressions()
        self.assertEqual(
            sw.Utility.Log.RotatingLogReader(logpath).ToString(),
            "1\n2\n3\n4\n5\n6\n"
        )
    
    def test_DelayedLog_withCompressedFiles(self):
        logpath = self.CreateLog_Delayed_WithCompressions()
        self.assertEqual(
            sw.Utility.Log.RotatingLogReader(logpath).ToString(),
            "1\n2\n3\n4\n5\n6\n7\n8\n9\n"
        )

    def test_OnlyCompressedFiles(self):
        logpath = self.CreateLog_WithCompression()
        self.assertEqual(
            sw.Utility.Log.RotatingLogReader(logpath).ToString(),
            "1\n2\n3\n4\n5\n6\n"
        )

class CustomSettingsManager_JSON_WithDefaultValues(SettingsManager_JSON):
    Settings = {
        "testString": "str1",
        "testInt": 10,
        "testBool": True,
        "testList": ["a", "b", "c", [{"a2": 100}]]
    }
class CustomSettingsManager_Automapped_TypedSettings(SettingsManager_AutoMapped_JSON):
    Setting_testString = "str1"
    Setting_testInt = 10
    Setting_testBool = True
    Setting_testList = ["a", "b", "c", [{"a2": 100}]]
class SettingsProvidersTests(BaseTestCase):
    
    testSettingsPath = os.path.join(BaseTestCase.testPath, "settings.anyextension")

    def test_SettingsManagerJSON_LoadsAndSavesCorrect(self):
        settingsManager = SettingsManager_JSON(self.testSettingsPath)
        assert len(settingsManager.Settings.keys()) ==  0
        settingsManager.LoadSettings()
        settingsManager.Settings["test1"] = 10
        settingsManager.Settings["test2"] = 20
        settingsManager.SaveSettings()
        savedSettingData = sw.IO.File.Read(settingsManager._settingsPath)
        obj = json.loads(savedSettingData)
        assert obj == {"test1": 10, "test2": 20}
        settingsManager = SettingsManager_JSON(settingsManager._settingsPath)
        settingsManager.LoadSettings()
        assert settingsManager.Settings["test1"] ==  10
        assert settingsManager.Settings["test2"] ==  20

    def test_SettingsManagerWithDynamicSettings_LoadsCorrectly(self):
        settingsManager = CustomSettingsManager_JSON_WithDefaultValues(self.testSettingsPath)
        settingsManager.LoadSettings()  # nothing to load, should keep default settings
        assert settingsManager.Settings["testString"] ==  "str1"
        assert settingsManager.Settings["testInt"] ==  10
        assert settingsManager.Settings["testBool"] ==  True
        assert settingsManager.Settings["testList"][0] ==  "a"
        assert settingsManager.Settings["testList"][3][0]["a2"] ==  100
        settingsManager.SaveSettings()

        # should still load the default settings that were saved previously
        settingsManager = CustomSettingsManager_JSON_WithDefaultValues(settingsManager._settingsPath)
        settingsManager.LoadSettings()  # should load same as default settings
        assert settingsManager.Settings["testString"] ==  "str1"
        assert settingsManager.Settings["testInt"] ==  10
        assert settingsManager.Settings["testBool"] ==  True
        assert settingsManager.Settings["testList"][0] ==  "a"
        assert settingsManager.Settings["testList"][3][0]["a2"] ==  100

        sw.IO.File.Create(settingsManager._settingsPath, json.dumps({"testInt": 999}))
        settingsManager = CustomSettingsManager_JSON_WithDefaultValues(settingsManager._settingsPath)
        settingsManager.LoadSettings()  # should load "testInt", should keep default settings
        assert settingsManager.Settings["testString"] ==  "str1"
        assert settingsManager.Settings["testInt"] ==  999
        assert settingsManager.Settings["testBool"] ==  True
        assert settingsManager.Settings["testList"][0] ==  "a"
        assert settingsManager.Settings["testList"][3][0]["a2"] ==  100

        settingsManager.Settings["testList"][3][0]["a2"] = 200
        assert settingsManager.Settings["testList"][3][0]["a2"] ==  200
        settingsManager.ClearSettings() #should restore default value, to ensure not same reference was used
        assert settingsManager.Settings["testList"][3][0]["a2"] ==  100

    def test_SettingsManagerWithTypedSettings_LoadsCorrectly(self):
        settingsManager = CustomSettingsManager_Automapped_TypedSettings(self.testSettingsPath)
        settingsManager.LoadSettings()  # nothing to load, should keep default settings
        assert settingsManager.Setting_testString ==  "str1"
        assert settingsManager.Setting_testInt ==  10
        assert settingsManager.Setting_testBool ==  True
        assert settingsManager.Setting_testList[0] ==  "a"
        assert settingsManager.Setting_testList[3][0]["a2"] ==  100
        settingsManager.SaveSettings()

        # should still load the default settings that were saved previously
        settingsManager = CustomSettingsManager_Automapped_TypedSettings(settingsManager._settingsPath)
        settingsManager.LoadSettings()  # should load same as default settings
        assert settingsManager.Setting_testString ==  "str1"
        assert settingsManager.Setting_testInt ==  10
        assert settingsManager.Setting_testBool ==  True
        assert settingsManager.Setting_testList[0] ==  "a"
        assert settingsManager.Setting_testList[3][0]["a2"] ==  100

        sw.IO.File.Create(settingsManager._settingsPath, json.dumps({"testInt": 999}))
        settingsManager = CustomSettingsManager_Automapped_TypedSettings(settingsManager._settingsPath)
        settingsManager.LoadSettings()  # should load same all default except "testInt"
        assert settingsManager.Setting_testString ==  "str1"
        assert settingsManager.Setting_testInt ==  999
        assert settingsManager.Setting_testBool ==  True
        assert settingsManager.Setting_testList[0] ==  "a"
        assert settingsManager.Setting_testList[3][0]["a2"] ==  100

        settingsManager.Setting_testList[3][0]["a2"] = 200
        assert settingsManager.Setting_testList[3][0]["a2"] ==  200
        settingsManager.ClearSettings() #should restore default value, to ensure not same reference was used
        assert settingsManager.Setting_testList[3][0]["a2"] ==  100
    
    def test_SettingsManager_BasicConfigParser_ParsesAndSavesProperly(self):
        settingsManager = SettingsManager_BasicConfig(self.testSettingsPath)
        settingsManager.LoadSettings()
        assert len(settingsManager.Settings.keys()) == 0

        settingsManager.Settings["key1"] = "value1"
        settingsManager.Settings["key2"] = "value2"
        settingsManager.SaveSettings()

        outputData = sw.IO.File.Read(self.testSettingsPath)
        assert sw.Utility.Regex.Match("/^key1=value1$/", outputData)
        assert sw.Utility.Regex.Match("/^key2=value2$/", outputData)

    def test_SettingsManager_BasicConfigParser_HandlesCommentsCorrectly(self):
        # try parse a new file
        configFileData = "\n" #empty line
        configFileData += "# start comment\n"
        configFileData += " # also a comment, since whitespace are stripped\n"
        configFileData += "\n"
        configFileData += "#key1 comment\n"
        configFileData += "key1=value1         # inline comment\n"
        configFileData += "#key2 comment, here we add some spacing to ensure its not affected\n"
        configFileData += "  key2   =    value2     \n" #should be "key2": "value2"
        configFileData += "\n"
        configFileData += "### when you add new settings, they should be added below this comment ###\n"
        sw.IO.File.Create(self.testSettingsPath, configFileData)
        settingsManager = SettingsManager_BasicConfig(self.testSettingsPath)
        settingsManager.LoadSettings()
        assert len(settingsManager.Settings.keys()) == 2
        assert settingsManager.Settings["key1"] == "value1"
        assert settingsManager.Settings["key2"] == "value2"

        #try export the config
        settingsManager.SaveSettings()
        outputLines = sw.IO.File.Read(self.testSettingsPath).splitlines()
        assert outputLines[0] == ""
        assert outputLines[1] == "# start comment"
        assert outputLines[2] == "# also a comment, since whitespace are stripped" # here the saved version should have left whitespace stripped
        assert outputLines[3] == ""
        assert outputLines[4] == "#key1 comment"
        assert outputLines[5] == "key1=value1 # inline comment"
        assert outputLines[6] == "#key2 comment, here we add some spacing to ensure its not affected"
        assert outputLines[7] == "key2=value2" # all whitespaces stripped
        assert outputLines[8] == ""
        assert outputLines[9] == "### when you add new settings, they should be added below this comment ###"

        #add non existing settings before save to ensure they are added last
        settingsManager = SettingsManager_BasicConfig(self.testSettingsPath)
        settingsManager.LoadSettings()
        assert len(settingsManager.Settings.keys()) == 2
        assert settingsManager.Settings["key1"] == "value1"
        assert settingsManager.Settings["key2"] == "value2"

        settingsManager.Settings["key3"] = "value3"
        settingsManager.Settings["key4"] = "value4"
        settingsManager.SaveSettings()
        outputLines = sw.IO.File.Read(self.testSettingsPath).splitlines()
        assert len(outputLines) == 12
        assert outputLines[0] == ""
        assert outputLines[1] == "# start comment"
        assert outputLines[2] == "# also a comment, since whitespace are stripped" # here the saved version should have left whitespace stripped
        assert outputLines[3] == ""
        assert outputLines[4] == "#key1 comment"
        assert outputLines[5] == "key1=value1 # inline comment"
        assert outputLines[6] == "#key2 comment, here we add some spacing to ensure its not affected"
        assert outputLines[7] == "key2=value2" # all whitespaces stripped
        assert outputLines[8] == ""
        assert outputLines[9] == "### when you add new settings, they should be added below this comment ###"
        
        newdata = '\n'.join(outputLines[10:12])
        assert sw.Utility.Regex.Match("/^key3=value3$/",newdata)
        assert sw.Utility.Regex.Match("/^key4=value4$/",newdata)

        settingsManager = SettingsManager_BasicConfig(self.testSettingsPath)
        settingsManager.LoadSettings()
        assert len(settingsManager.Settings.keys()) == 4
        assert settingsManager.Settings["key1"] == "value1"
        assert settingsManager.Settings["key2"] == "value2"
        assert settingsManager.Settings["key3"] == "value3"
        assert settingsManager.Settings["key4"] == "value4"
        del settingsManager.Settings["key1"]
        del settingsManager.Settings["key3"]

        settingsManager.SaveSettings()
        outputLines = sw.IO.File.Read(self.testSettingsPath).splitlines()
        assert len(outputLines) == 10
        assert outputLines[0] == ""
        assert outputLines[1] == "# start comment"
        assert outputLines[2] == "# also a comment, since whitespace are stripped" # here the saved version should have left whitespace stripped
        assert outputLines[3] == ""
        assert outputLines[4] == "#key1 comment"
        assert outputLines[5] == "#key2 comment, here we add some spacing to ensure its not affected"
        assert outputLines[6] == "key2=value2" # all whitespaces stripped
        assert outputLines[7] == ""
        assert outputLines[8] == "### when you add new settings, they should be added below this comment ###"
        assert outputLines[9] == "key4=value4"

    @unittest.skip
    def test_SettingsManager_BasicConfigParser_PerformanceTesting(self):
        def CreateDummySettings():
            with open(self.testSettingsPath, "w") as fp:
                fp.write(f"[DEFAULT]\n")
                for i in range(100):
                    fp.write(f"key{i}=value{i}\n")

        sw1 = sw.Utility.StopWatch()
        sw2 = sw.Utility.StopWatch()
        sw3 = sw.Utility.StopWatch()
        sw4 = sw.Utility.StopWatch()



        for i in range(100):
            CreateDummySettings()
            sw1.Start()
            settingsManager = sw.SettingsProviders.SettingsManager_BasicConfig("./out/settings.anyextension")
            settingsManager.LoadSettings()
            sw1.Stop()
            sw2.Start()
            settingsManager.SaveSettings()
            sw2.Stop()

            CreateDummySettings()
            sw3.Start()
            cnf = ConfigParser()
            cnf.read("./out/settings.anyextension")
            sw3.Stop()
            sw4.Start()
            with open("./out/settings.anyextension", "w") as f:
                cnf.write(f)
            sw4.Stop()

        result = f"basicConfig: {sw1.GetElapsedMilliseconds()} - {sw2.GetElapsedMilliseconds()} \n"
        result += f"python ConfigParser: {sw3.GetElapsedMilliseconds()} - {sw4.GetElapsedMilliseconds()} "
        assert 1 == 0, result