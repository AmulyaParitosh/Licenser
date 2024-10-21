# Licenser

Licenser is a powerful and flexible command-line utility for creating LICENSE files and adding license headers to your project files on the fly. Built with Python, it's designed to streamline the process of managing licenses across your projects, regardless of your operating system.

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/AmulyaParitosh/Licenser)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

## Table of Contents

- [Licenser](#licenser)
	- [Table of Contents](#table-of-contents)
	- [Features](#features)
	- [Supported Licenses](#supported-licenses)
	- [Installation](#installation)
	- [Usage](#usage)
		- [Creating a License File](#creating-a-license-file)
		- [Adding License Headers](#adding-license-headers)
		- [Generating a Config File](#generating-a-config-file)
	- [Examples](#examples)
	- [Contributing](#contributing)
	- [License](#license)

## Features

- Generate LICENSE files for various open-source licenses
- Add license headers to multiple files simultaneously
- Cross-platform compatibility (works on any system with Python)
- Interactive mode for guided license creation
- Regex-based file matching for adding headers
- Customizable author, email, and year information

## Supported Licenses

Licenser supports the following licenses:

| SPDX Identifier | License Name |
|-----------------|--------------|
| AGPL-3.0 | GNU Affero General Public License v3.0 |
| Apache-2.0 | Apache License 2.0 |
| BSD-2-Clause | BSD 2-Clause "Simplified" License |
| BSD-3-Clause | BSD 3-Clause "New" or "Revised" License |
| BSL-1.0 | Boost Software License 1.0 |
| CC0-1.0 | Creative Commons Zero v1.0 Universal |
| EPL-2.0 | Eclipse Public License 2.0 |
| GPL-2.0 | GNU General Public License v2.0 |
| GPL-3.0 | GNU General Public License v3.0 |
| LGPL-2.1 | GNU Lesser General Public License v2.1 |
| MIT | MIT License |
| MPL-2.0 | Mozilla Public License 2.0 |
| Unlicense | The Unlicense |


## Supported Programming Languages for SPDX Headers

Licenser is compatible with the following programming language file formats for adding SPDX headers:

- JavaScript (`js`): `/*{}*/`
- Java (`java`): `/*{}*/`
- C (`c`): `/*{}*/`
- C++ (`cpp`): `/*{}*/`
- C# (`cs`): `/*{}*/`
- PHP (`php`): `/*{}*/`
- Ruby (`rb`): `=begin\n{}\n=end`
- Swift (`swift`): `/*{}*/`
- Kotlin (`kt`): `/*{}*/`
- HTML (`html`): `<!--{}-->`
- CSS (`css`): `/*{}*/`
- SQL (`sql`): `/*{}*/`
- Bash (`sh`): `: '{}'`
- Go (`go`): `/*{}*/`
- R (`r`): `# {}`
- Python (`py`): `# {}`
- MATLAB (`m`): `%{{\n{}\n%}}`
## Installation

You can install Licenser directly from GitHub using pip:

```bash
pip install git+https://github.com/AmulyaParitosh/Licenser.git
```

This will install Licenser and its dependencies on your system.

## Usage

Licenser provides three main commands: `create`, `header`, and `generate_config`. Here's how to use each of them:

### Creating a License File

To create a license file, use the `create` command:

```bash
licenser create [-h] [-i] [--author AUTHOR] [--email EMAIL] [--year YEAR] [-o] LICENSE_IDENTIFIER
```

Options:
- `-h`, `--help`: Show help message and exit
- `-i`, `--interactive`: Interactive mode
- `--author AUTHOR`: Specify author name
- `--email EMAIL`: Specify author email
- `--year YEAR`: Specify year
- `-o`, `--overwrite`: Overwrite existing LICENSE file

`LICENSE_IDENTIFIER` should be one of the supported SPDX identifiers (e.g., MIT, GPL-3.0, etc.).

### Adding License Headers

To add license headers to files, use the `header` command:

```bash
licenser header [-h] [-d] path regex
```

Arguments:
- `path`: Path to add license header to
- `regex`: Regex pattern to match files

Options:
- `-h`, `--help`: Show help message and exit
- `-d`, `--dir`: Add license header to all files in directory

### Generating a Config File

To generate a default configuration file, use the `generate_config` command:

```bash
licenser generate_config [-h]
```

This command generates a default config file if one doesn't already exist.

## Examples

1. Create an MIT license file interactively:
   ```bash
   licenser create MIT -i
   ```

2. Create a GPL-3.0 license file with specific author information:
   ```bash
   licenser create GPL-3.0 --author "John Doe" --email "john@example.com" --year 2023
   ```

3. Add license headers to all Python files in a directory:
   ```bash
   licenser header ./src ".*\.py$" -d
   ```

4. Generate a default configuration file:
   ```bash
   licenser generate_config
   ```

## Contributing

Contributions to Licenser are welcome! If you have suggestions for improvements or bug fixes, please feel free to:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
