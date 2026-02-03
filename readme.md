# OBS Floater


**OBS Floater** is a lightweight, floating status bar for OBS that displays real-time recording and streaming status overlay designed specifically for single-monitor streamers and recorders.

🎬 [OBS Floater Demo](https://youtu.be/edJDNuTKM0E) 

Preview on 2560x1440 screen.
![OBS Floater Preview](obs-floater-preview.jpg)

## Requirements

Before running the script, ensure you have the following installed on your system:

1. **Python 3.11.x** (Ensure it is added to your System PATH).
2. **PyQt6**: For the graphical interface.
3. **obs-websocket-py**: For communicating with OBS.
4. Currently only support **Windows**.

### Installation Command

To install the requirement, open your terminal (CMD) and run:

```bash
pip install PyQt6 obs-websocket-py
```

## Setup

1. Prepare the Scripts. Ensure both `obs_floater.py` and `floater_launcher.py` are in the same folder. You can place these file in any folder.
2. Open `floater_launcher.py` and ensure `PYTHON_EXE` points to **your** local Python installation. Use the command `where pythonw` in your terminal to find your path.
3. Open `obs_floater.py`, change your OBS WebSocket Password. If you don't use password just leave it blank. 

## OBS Configuration

### Enable WebSocket

1. Open **OBS Studio**.
2. Go to **Tools** -> **WebSocket Server Settings**.
3. Check **Enable WebSocket server**.
4. Note the **Server Port** (default is 4455) and the **Server Password**.

### Link Python to OBS

1. Go to **Tools** -> **Scripts**.
2. Click the **Python Settings** tab.
3. Browse and select your Python install path.
    - *Example path:* `C:\Users\<YourUser>\AppData\Local\Programs\Python\Python311`

## Customization

- **Position:** Look at launcher_pro.py Edit `self.move(x, y)` in `obs_floater.py` to change where the bar appears on your screen.
- **Size:** Edit `self.setFixedSize(width, height)` to change the bar dimensions.
- **Colors:** You can modify the HEX codes (e.g., `#ff4d4d` for red) in the `update_styles` function.

## Shameless Promotion

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/D1D41SPX1E)

👍 Subscribe to [OpenQuestline](https://www.youtube.com/channel/UC3SxeNanAnhtBQMuBbrskdg/?sub_confirmation=1). My small game guide channel.  
🐦 Follow me on [X](https://x.com/kuswanto). 🧵 Follow me on [Threads](https://www.threads.com/@ncus).

## License

Change from MIT to GPL V2 to comply with OBS plugins license.