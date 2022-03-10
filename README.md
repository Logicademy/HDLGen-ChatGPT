# HDLGen

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

### Using the Application
1. When creating a new project make sure to click on save in the project manager before navigating to design tab.

### Screenshots
#### Project Manager
<img src="https://github.com/abishek-bupathi/HDLGen/blob/83c569e9b708c27212a69c125e69bcc74a5cb2ac/Docs/Screenshots/Project%20Manager%20v1.png" width="700"></img>

#### Design

##### Component details
<img src="https://github.com/abishek-bupathi/HDLGen/blob/692434cfc7d68ff379cdc9abe3e9e324f68e444c/Docs/Screenshots/Design-comp_details.png" width="700"></img>

##### Port IO Signals
**Add New Signals**

<img src="https://github.com/abishek-bupathi/HDLGen/blob/692434cfc7d68ff379cdc9abe3e9e324f68e444c/Docs/Screenshots/design-io_ports-add_signal.png" width="300"></img>

**IO Signal List**

<img src="https://github.com/abishek-bupathi/HDLGen/blob/692434cfc7d68ff379cdc9abe3e9e324f68e444c/Docs/Screenshots/design-io_ports-signal_list.png" width="700"></img>


### To Do

- [ ] Design Tab UI in PySide
- [ ] Read and write Design XML

### In Progress

- [ ] I/O Ports
  - [x] Add signal button
  - [ ] inout mode addition 
  - [x] Save button
  - [x] Signal List
  - [x] Delete signal button
  - [x] Signal mode
  - [x] Signal Name
  - [x] Signal Type
  - [x] Description
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
- [ ] Design Tab UI
  - [x] Header details
  - [x] I/O Ports
  - [ ] Architecture
  - [ ] Clk and Rst
- [ ] Render Markdown in help Tab
  - [x] Render basic md
  - [ ] Render tables
  - [ ] Render code block
- [ ] Welcome screen
  - [x] New Project
  - [x] Open Project
  - [ ] Welcome Info

### Completed

- [x] Component details
  - [x] Get data from input
  - [x] Update preview
- [x] Read XML file and populate details
- [x] Write Tool Version to xml
- [x] Write Tool dir to xml
- [x] Write languages to xml 
- [x] Add borders to UI 
- [x] Generate folders from XML 

