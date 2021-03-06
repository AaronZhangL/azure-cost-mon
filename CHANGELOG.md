Change Log
==========

All notable changes to this project are noted in this file. This project adheres to [Semantic
Versioning](http://semver.org/).

0.4.1
-----

- Fixed issue (https://github.com/blue-yonder/azure-cost-mon/issues/12)
  where the sum of multiple time series was numerically instable by
  emitting only integer values. The instability resulted in more counter
  resets within Prometheus than necessary, so that `increase` gave wrong
  results!


0.4.0
-----

- Use the `X-Prometheus-Scrape-Timeout-Seconds` header sent by
  prometheus to overwrite the internal request timeout default.


0.3.1
-----

- Fixed the exporter to cope with the non-standard response for months
  without usage details.


0.3.0
-----

- Removed own metric implementation in favor of the
  official prometheus_client
- Made metrics name non-optional in the configuration to prevent
  non standard metric name (w/o unit).
- Adapted README to match the package renaming

0.2
---

- Initial version

