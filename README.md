# HDLGen

### Screenshots
<img src="https://github.com/abishek-bupathi/HDLGen/blob/83c569e9b708c27212a69c125e69bcc74a5cb2ac/Docs/Screenshots/Project%20Manager%20v1.png" width="700"></img>

### Project Setup
1. Install Python v3.9
2. Clone the repository
``
git clone https://github.com/abishek-bupathi/HDLGen.git
``
3. Open the project in IntelliJ PyCharm or VSCode
4. Install required libraries
``
pip install -r requirements.txt
``
5. Run main.py

Using the Application
1. When creating a new project make sure to click on save in the project manager before navigating to design tab.

### To Do

- [ ] Design Tab UI in PySide
- [ ] Read and write Design XML

### In Progress

- [ ] Component details
  - [ ] Get data from input
  - [ ] Update preview
- [ ] Architecture Details
  - [ ] UI
  - [ ] Write data into XML
  - [ ] Update preview
- [ ] Design Tab XML structure
  - [x] Entity and Header
  - [x] Clk and Rst
  - [x] Input/Output Signals
  - [x] Architecture name
  - [x] Process
  - [ ] Concurrent statement
  - [ ] State reg
  - [ ] FSM
- [ ] Generate VHDL File
  - [x] Header comment
  - [x] Input/Output Signals
  - [x] Architecture name
  - [x] Default Initializations
  - [x] Process
  - [ ] Concurrent statements
  - [ ] clk and rst
  - [ ] state reg
  - [ ] FSM
- [ ] VHDL statements Database XML
  - [x] Header comment
  - [x] Input/Output Signals
  - [x] Architecture name
  - [x] Default Initializations
  - [x] Process
  - [ ] Concurrent statements
  - [ ] clk and rst
  - [ ] state reg
  - [ ] FSM
- [ ] Design Tab UI design
- [ ] Render Markdown in help Tab
  - [x] Render basic md
  - [ ] Render tables
  - [ ] Render code block

### Completed

- [x] Read XML file and populate details
- [x] Write Tool Version to xml
- [x] Write Tool dir to xml
- [x] Write languages to xml 
- [x] Add borders to UI 
- [x] Generate folders from XML 

