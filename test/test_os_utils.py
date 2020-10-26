from unittest import TestCase

import os
import tempfile
import __os_utils__ as osu

class OSUtilsTest(TestCase):
    '''
    Test the functions from the __os_utils__ module
    '''

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def _file_exists(self, path):
        return os.path.exists(path)

    def _create_test_files_in_test_dir(self):
        # Create a file per audio extension
        for ext in osu.audio_extensions:
            with open(os.path.join(self.test_dir, 'test' + ext), 'w') as f:
                f.write('Fufu')
        
        # Add a non audio file
        with open(os.path.join(self.test_dir, 'test.txt'), 'w') as f:
            f.write('Fefe')


    def test_audio_extensions(self):
        self.assertIn('.mp3', osu.audio_extensions)
        self.assertIn('.wav', osu.audio_extensions)
        self.assertIn('.flac', osu.audio_extensions)
        self.assertIn('.ogg', osu.audio_extensions)

    def test_filename(self):
        filename = 'test.wav'
        path = os.path.join('/home/user/music', filename)
        
        self.assertEqual(filename, osu.filename(path))

    def test_file_extension(self):
        extension = '.wav'
        filename = 'test' + extension
        path = os.path.join('/home/user/music', filename)

        self.assertEqual(extension, osu.file_extension(path))

    def test_create_dir(self):
        # Create a new directory
        dir_path = os.path.join(self.test_dir, 'test')
        self.assertFalse(self._file_exists(dir_path))
        osu.create_dir(dir_path)
        self.assertTrue(self._file_exists(dir_path))

        # Directory already exists
        osu.create_dir(dir_path)
        self.assertTrue(self._file_exists(dir_path))

    def test_create_dir_dry_run(self):
        dir_path = os.path.join(self.test_dir, 'test')
        self.assertFalse(self._file_exists(dir_path))
        osu.create_dir(dir_path, dry_run=True)
        self.assertFalse(self._file_exists(dir_path))

    def test_get_audio_files(self):
        self._create_test_files_in_test_dir()

        audio_files = osu.get_audio_files(self.test_dir)
        self.assertEquals(len(audio_files), len(osu.audio_extensions))

    def test_move_files(self):
        self._create_test_files_in_test_dir()

        # Create the target directory
        target_dir = os.path.join(self.test_dir, 'target')
        osu.create_dir(target_dir)
        
        # Move the files
        for f in os.listdir(self.test_dir):
            f_path = os.path.join(self.test_dir, f)

            # target_dir is inside test_dir
            if f_path != target_dir:
                self.assertTrue(self._file_exists(f_path))
                osu.move_file(f_path, target_dir)
                self.assertFalse(self._file_exists(f_path))
                self.assertTrue(self._file_exists(os.path.join(target_dir, f)))
                