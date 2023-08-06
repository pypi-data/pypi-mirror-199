# uptimecurl

Basic monitoring tool designed for rapid deployment and simple results.

Scheduled monitoring, dashboards, alerts and other advanced features are out of
scope. Instead consider tools like crontab, Cockpit, Grafana or Zabbix.

## Usage

```
Usage: uptimecurl [OPTIONS]

  Basic monitoring tool designed for rapid deployment and simple results.

  Define tests in the DEFINITION file and template in the TEMPLATE file.
  Report is generated at the OUTPUT path.

  Instead of command-line parameters you can use the environment variables
  UPTIMECURL_DEFINITION, UPTIMECURL_TEMPLATE and UPTIMECURL_OUTPUT. These
  can be defined in a .env file in the working directory.

Options:
  --definition FILE  List of test definitions (YAML).
  --template FILE    Template to generate report from test results (Mustache).
  --output FILE      Output path for report (typically HTML).
  --help             Show this message and exit.
```

### Sample definition

```
example_http:
    type: http_ok
    parameters:
      - http://en.wikipedia.org
example_port:
    type: port_ok
    parameters:
      - en.wikipedia.org
      - 443
```

### Sample template

See <https://mustache.github.io/mustache.5.html> for template language.

```
<tbody>
{{#data}}
  <tr>
    <td title="{{timestamp}}">
      {{name}}
    </td>
    <td title="{{parameters}}">
      {{type}}
    </td>
    <td title="{{message}}">
      {{success_code}}
    </td>
  </tr>
{{/data}}
</tbody>
```

### Sample report

Run `uptimecurl` without parameters to generate this sample report in HTML
(hover or view source on each cell for more detail):

<table>
  <thead>
    <tr>
      <th>
        Name
      </th>
      <th>
        Test
      </th>
      <th>
        Result
      </th>
    </tr>
  </thead>
  <tbody>
      <tr>
        <td title="2020-09-03 16:28:42.416792">
          example_http
        </td>
        <td title="['http://en.wikipedia.org']">
          http_ok
        </td>
        <td title="http://en.wikipedia.org returned 301">
          ❌
        </td>
      </tr>
      <tr>
        <td title="2020-09-03 16:28:42.449334">
          example_port
        </td>
        <td title="['en.wikipedia.org', 443]">
          port_ok
        </td>
        <td title="">
          💚
        </td>
      </tr>
  </tbody>
</table>

### Test types

#### http_ok

```
test_name:
    type: http_ok
    parameters:
      - https://example.com/path
```

Perform an HTTP request against any URL (parameter 0).

Return 💚 if we get a `200 OK` response, ❌ otherwise.

Note that we expect strictly a `200 OK` reponse. Redirects and other values
will result in a failure. (See the sample report for an example of a failure.)

#### port_ok

```
test_name:
    type: port_ok
    parameters:
      - domain.com
      - 1234
```

Attempt to connect to `domain:port` (parameter 0, parameter 1).

Return 💚 if successful, ❌ otherwise.

Note that an open port does not guarantee that the underlying application is
working, just that the server is up and correctly configured.

<!-- start @generated footer -->

# Development environment

## Install prerequisites

- Python 3.10
- pdm
- make

## Instructions

- Fork the upstream repository.
- `git clone [fork-url]`
- `cd [project-folder]`
- Run `make develop` to initialise your development environment.

You can use any text editor or IDE that supports virtualenv / pdm. See the
Makefile for toolchain details.

Please `make test` and `make lint` before submitting changes.

## Make targets

```
USAGE: make [target]

help    : Show this message.
develop : Set up Python development environment.
run     : Run from source.
clean   : Remove all build artefacts.
test    : Run tests and generate coverage report.
lint    : Fix or warn about linting errors.
build   : Clean, test, lint, then generate new build artefacts.
publish : Upload build artefacts to PyPI.
```

# Sharing and contributions

```
uptimecurl
https://lofidevops.neocities.org
Copyright 2020 David Seaward and contributors
SPDX-License-Identifier: AGPL-3.0-or-later
```

Shared under AGPL-3.0-or-later. We adhere to the Contributor Covenant 2.1, and
certify origin per DCO 1.1 with a signed-off-by line. Contributions under the
same terms are welcome.

Submit security and conduct issues as private tickets. Sign commits with
`git commit --signoff`. For a software bill of materials run `reuse spdx`. For
more details see CONDUCT, COPYING and CONTRIBUTING.
