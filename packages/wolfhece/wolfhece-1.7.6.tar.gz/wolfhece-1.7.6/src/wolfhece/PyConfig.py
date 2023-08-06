import os
import json
from enum import Enum
from pathlib import Path

import wx
from .PyTranslate import _

class ConfigurationKeys(Enum):
    """ Using enumerated keys make sure we
    can check value names at write time
    (i.e. we don't use string which are brittle)
    """
    VERSION = "Version"
    PLAY_WELCOME_SOUND = "PlayWelcomeSound"


class WolfConfiguration:
    """ Holds the PyWolf configuration.
    """

    def __init__(self, path=None):
        # We make sure we use a standard location
        # to store the configuration
        if path is None:
            if os.name == "nt":
                # On Windows NT, LOCALAPPDATA is expected to be defined.
                # (might not be true in the future, who knows)
                self._options_file_path = Path(os.getenv("LOCALAPPDATA")) / "wolf.conf"
            else:
                self._options_file_path = Path("wolf.conf")
        else:
            self._options_file_path = path

        if self._options_file_path.exists():
            self.load()
        else:
            self.set_default_config()
            # This save is not 100% necessary but it helps
            # to make sure a config file exists.
            self.save()

    @property
    def path(self) -> Path:
        """ Where the configuration is read/saved."""
        return self._options_file_path

    def set_default_config(self):
        self._config = {
            ConfigurationKeys.VERSION.value: 1,
            ConfigurationKeys.PLAY_WELCOME_SOUND.value: True
        }
        self._check_config()

    def _check_config(self):
        assert type(self._config[ConfigurationKeys.PLAY_WELCOME_SOUND.value]) == bool

    def load(self):
        with open(self._options_file_path, "r", encoding="utf-8") as configfile:
            self._config = json.loads(configfile.read())
        self._check_config()

    def save(self):
        # Make sure to write the config file only if it can
        # be dumped by JSON.
        txt = json.dumps(self._config, indent=1)
        with open(self._options_file_path, "w", encoding="utf-8") as configfile:
            configfile.write(txt)

    def __getitem__(self, key: ConfigurationKeys):
        assert isinstance(key, ConfigurationKeys), "Please only use enum's for configuration keys."
        return self._config[key.value]

    def __setitem__(self, key: ConfigurationKeys, value):
        # A half-measure to ensure the config structure
        # can be somehow validated before run time.
        assert isinstance(key, ConfigurationKeys), "Please only use enum's for configuration keys."

        self._config[key.value] = value
        self._check_config()


class GlobalOptionsDialog(wx.Dialog):

    def __init__(self, *args, **kw):
        super(GlobalOptionsDialog, self).__init__(*args, **kw)

        self.InitUI()
        self.SetSize((250, 200))
        self.SetTitle("Change Color Depth")

    def push_configuration(self, configuration):
        self.cfg_welcome_voice.SetValue(configuration[ConfigurationKeys.PLAY_WELCOME_SOUND])

    def pull_configuration(self, configuration):
        configuration[ConfigurationKeys.PLAY_WELCOME_SOUND] = self.cfg_welcome_voice.IsChecked()


    def InitUI(self):

        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        sb = wx.StaticBox(pnl, label='Miscellaneous')
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)
        self.cfg_welcome_voice = wx.CheckBox(pnl, label='Welcome voice')
        sbs.Add(self.cfg_welcome_voice)

        pnl.SetSizer(sbs)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, wx.ID_OK, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox2.Add(okButton)
        hbox2.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(pnl, proportion=1,
            flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox2, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.SetSizer(vbox)

        okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)

    def OnOk(self, e):
        if self.IsModal():
            self.EndModal(wx.ID_OK)
        else:
            self.Close()

    def OnClose(self, e):
        self.Destroy()

def handle_configuration_dialog(wxparent, configuration):
    dlg = GlobalOptionsDialog(wxparent)
    try:
        dlg.push_configuration(configuration)

        if dlg.ShowModal() == wx.ID_OK:
            # do something here
            dlg.pull_configuration(configuration)
            configuration.save()
            wx.LogMessage(_('Configuration saved in {}').format(str(configuration.path)))
        else:
            # handle dialog being cancelled or ended by some other button
            pass
    finally:
        # explicitly cause the dialog to destroy itself
        dlg.Destroy()


if __name__ == "__main__":
    cfg = WolfConfiguration(Path("test.conf"))
    cfg[ConfigurationKeys.PLAY_WELCOME_SOUND] = False
    print(cfg._config)
    cfg.save()
    cfg = WolfConfiguration(Path("test.conf"))
    cfg.load()
    print(cfg[ConfigurationKeys.PLAY_WELCOME_SOUND])
