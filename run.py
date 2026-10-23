"""
Autonomous Crypto Trading Robot Terminal
Launch script for 24x7 web dashboard and execution engine.
"""

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from crypto_robot.app import app

if __name__ == "__main__":
    print("=" * 65)
    print(" RIM Autonomous Crypto Trading Terminal")
    print(" 24x7 High-Probability Dynamic Trailing Engine")
    print(" Web Dashboard: http://127.0.0.1:5055")
    print("=" * 65)
    app.run(host="0.0.0.0", port=5055, debug=False)
