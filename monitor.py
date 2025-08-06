name: Labubu Stock Monitor

on:
  schedule:
    - cron: "*/10 * * * *"   # 每 10 分钟跑一次
  workflow_dispatch:
    inputs:
      test_mode:
        description: "是否启用演示模式？"
        required: false
        default: "false"

jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: pip install requests beautifulsoup4

      - name: Run monitor
        env:
          DISCORD_WEBHOOK: ${{ secrets.DISCORD_WEBHOOK }}
          TEST_MODE: ${{ github.event.inputs.test_mode || 'false' }}
        run: python monitor.py
