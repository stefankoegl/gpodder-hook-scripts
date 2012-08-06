#!/usr/bin/python
# -*- coding: utf-8 -*-
import filecmp
import os
import shutil
import unittest

import gpodder

from config import data
import utils

EXTENSION_NAME = 'normalize_audio'
EXTENSION_FILE = os.path.join(os.environ['GPODDER_EXTENSIONS'], EXTENSION_NAME+'.py')


class TestNormalizeAudio(unittest.TestCase):
    def setUp(self):
        self.core, podcast_list = utils.init_test(
            EXTENSION_FILE,
            [(data.TEST_PODCASTS['DeimHart'], True),
             (data.TEST_PODCASTS['TinFoilHat'], True),
             (data.TEST_PODCASTS['drovics'], True)
            ]
        )
        (self.ogg_episode, self.ogg_file, self.mp3_episode,
            self.mp3_file, self.flv_episode, self.flv_file)  = podcast_list
        self.ogg_file_save = self.save_episode(self.ogg_file)
        self.mp3_file_save = self.save_episode(self.mp3_file)
        self.flv_file_save = self.save_episode(self.flv_file)

        self.core.config.extensions.enabled = [EXTENSION_NAME]

    def tearDown(self):
        shutil.move(self.ogg_file_save, self.ogg_file)
        shutil.move(self.mp3_file_save, self.mp3_file)
        shutil.move(self.flv_file_save, self.flv_file)

        self.core.shutdown()

    def save_episode(self, episode_name):
        filename_save = '%s.save' % episode_name
        shutil.copyfile(episode_name, filename_save)
        return filename_save

    def test_mp3_file(self):
        self.assertTrue(filecmp.cmp(self.mp3_file, self.mp3_file_save))

        gpodder.user_extensions.on_episode_downloaded(self.mp3_episode)

        self.assertFalse(filecmp.cmp(self.mp3_file, self.mp3_file_save))

    def test_ogg_file(self):
        self.assertTrue(filecmp.cmp(self.ogg_file, self.ogg_file_save))

        gpodder.user_extensions.on_episode_downloaded(self.ogg_episode)

        self.assertFalse(filecmp.cmp(self.ogg_file, self.ogg_file_save))

    def test_context_menu(self):
        self.assertTrue(gpodder.user_extensions.on_episodes_context_menu([self.mp3_episode,]))
        self.assertTrue(gpodder.user_extensions.on_episodes_context_menu([self.ogg_episode,]))
        self.assertFalse(gpodder.user_extensions.on_episodes_context_menu([self.flv_episode,]))