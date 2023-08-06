# Indicator-Intelligence

#### NOTE : You should definitely use it for legal activities.

## Description

Indicator-Intelligence collects static files and related domains for target to do threat intelligence.


## Usage

```
-d DOMAINS [DOMAINS], --domains DOMAINS [DOMAINS] Input Targets. --domains target-web1.com target-web2.com
-p PROXY, --proxy PROXY Use HTTP proxy. --proxy 0.0.0.0:8080
-a AGENT, --agent AGENT Use agent. --agent 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
-o JSON, --json JSON  JSON output. --json
```

#### Function Usage

```
from indicator.indicator import Indicator

#SCAN
Indicator(["target-web.com"])

#OUTPUT
Indicator(["target-web.com"],json=True)
```

## License

Copyright (c) 2023 Osman Kandemir \
Licensed under the GPL-3.0 License.

## Donations
If you like Indicator-Intelligence and would like to show support, you can Buy A Coffee for the developer using the button below

<a href="https://www.buymeacoffee.com/OsmanKandemir" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

Your support will be much appreciated😊