# larzuk

A command-line tool to help modding-as-code for game Diablo II: Resurrected.

## How to Use

1. Install this command-line tool via `pip`:

    ```shell
    $ pip install larzuk
    ```
2. Write migration scripts in a directory (e.g. `migrations`):

    ```python
    # Relative path of .txt file you want to modify.
    target = 'global/excel/armor.txt'

    # Entry function of migration
    def migrate(txt_file):
        for row in txt_file:
            row['minac'] = row['maxac']
    ```

3. Run `larzuk` command to do migrations:

    ```shell
    $ larzuk up --target-dir /path/to/d2r/data
    ```

4. Check file `armor.txt` in data directory, values in column `minac` equal to `maxac`.

## Example

Check [https://github.com/he-yaowen/Lablo](https://github.com/he-yaowen/Lablo)

## License

Copyright (C) 2023 HE Yaowen <he.yaowen@hotmail.com>

The GNU General Public License (GPL) version 3, see [LICENSE](./LICENSE).
