# dropme
CLI tool to manage data in Dropbox workspace

## How to use
1. Clone `dropme` repository: `git clone https://github.com/tivaliy/dropme.git`.
2. Configure `settings.yaml` file (in `dropme/settings.yaml`).

    ```
    token: "YOUR_DROPBOX_ACCESS_TOKEN"
    ```

3. Create isolated Python environment `virtualenv venv` and activate it `source venv/bin/activate`.
4. Install `dropme` with all necessary dependencies: `pip install -r requirements.txt .`.
5. (Optional) Add `dropme` command bash completion:

    `dropme complete | sudo tee /etc/bash_completion.d/gc.bash_completion > /dev/null`

    Restart terminal and activate virtual environment once again.
6. Run `dropme`:

    * as a standalone application

        ```
        $ dropme
        (dropme) whoami
        |---------|------------------------|
        | Field   | Value                  |
        |---------|------------------------|
        | user    | John Doe               |
        | e_mail  | j.doe@example.com      |
        | country | UA                     |
        +---------+------------------------+
        ```

    * as a command with respective sub-command arguments

        ```
        $ dropme df
        |-----------|-----------------|
        | Field     | Value           |
        |-----------|-----------------|
        | allocated | 2.0 GB          |
        | used      | 1.11 MB (99.9%) |
        | available | 2.0 GB          |
        |-----------+-----------------|
        ```
