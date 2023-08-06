# release-finder

`release-finder` is a Python package that helps you find the latest releases information for a given GitHub repository.

## Installation

Install the `release-finder` using the package manager [pip](https://pip.pypa.io/en/stable/).

```bash
pip install release-finder
```

## Usage

```python
import release_finder

# returns 'v4.1.6'
release_finder.latest_release("https://github.com/utmapp/UTM")

# returns 'v4.1.6'
release_finder.latest_release("https://github.com/utmapp/UTM", "YOUR_ACCESS_TOKEN")

# returns '2023-02-27T02:28:31Z'
release_finder.latest_release_date("https://github.com/utmapp/UTM")

# returns '2023-02-27T02:28:31Z'
release_finder.latest_release_date("https://github.com/utmapp/UTM", "YOUR_ACCESS_TOKEN")
```

## Contributing

Pull requests are welcome. Please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
