- name: Checkout
  uses: actions/checkout@v2
  with:
    path: data
    ref: data # Branch name

- name: Set up Python
  uses: actions/setup-python@v2
  with:
    python-version: 3.7
    architecture: x64

- name: Push binary to data branch
  if: github.event_name == 'push'
  run: python master/.ci/move_binary.py "${{ steps.buildozer.outputs.filename }}" master data bin