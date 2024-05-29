# gm
GM Network

## Introduction

This software is designed to automate the process of registering accounts, collecting daily rewards, and completing tasks related to visiting pages. It does not currently support tasks on Discord, QuestN, or Twitter, but these features may be added in the future.

## Follow: https://t.me/esoteric_crypto_core

## Prerequisites

- Python 3.11 or higher
- A valid CAPTCHA solving service API key

## Installation

1. Clone this repository to your local machine.
    ```bash
    git clone https://github.com/Esoteric-crypto-core/gm.git
    cd gm
    ```

2. Create and activate a virtual environment:
   - On Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - On macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. Insert proxies and private keys into the files `proxy.txt` and `wallet.txt` respectively (located in the `files` folder).
2. Insert invite codes (any number, even one is fine) into the `invite_codes.txt` file (located in the `files` folder).
3. In the `config.py` file, configure the following:
   - `API_KEY`: Your CAPTCHA service API key.
   - `CAPTCHA_SERVICE`: The name of your CAPTCHA solving service (`anti-captcha`, `2captcha`).

## Usage

1. Run the software with the command:
    ```bash
    python main.py
    ```

2. Account information will be saved in the `data` table, and new invite codes will be saved in `new_codes.txt`.

## Troubleshooting

- If you encounter connection issues, ensure your proxies are working correctly and the target server is reachable.
- For SSL errors, check your SSL configuration and certificates.

## Donate
TRC-20: `TARuBWXr5yJHyhS9ZZF4RyqbUXQVWXQaUq`
ERC-20: `0xB333b6e713d5879109ceb884cc50a6b946D72C1D`

