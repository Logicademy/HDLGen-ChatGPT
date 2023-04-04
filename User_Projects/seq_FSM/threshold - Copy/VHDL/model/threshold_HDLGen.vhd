-- Header Section
-- Component Name : threshold
-- Title          : Generate a 32-x32-bit threshold array from 32x32-byte source data array

-- Description
-- Generate a 32-x32-bit threshold array from 
-- - 32x32-byte source data array
-- - threshVal(7:0)
-- 
-- Result bit is asserted if souce byte >= threshVal

-- Author(s)      : Fearghal Morgan
-- Company        : University of Galway
-- Email          : fearghal.morgan@universityofgalway.ie
-- Date           : 29/03/2023

-- entity signal dictionary
-- ce	threshold component enable. Assertion (h) activates the threshold register components.


-- go	Assertion (h) activates threshold finite state machine (FSM)


-- reg4x32_CSRA	4 x 32-bit register memory, control and status register A
-- reg4x32_CSRB	4 x 32-bit register memory, control and status register B
-- BRAM_dOut	256-bit block RAM (BRAM) memory


-- active	Asserted to highlight that FSM is active. Signal is a flag and is not used externally. 


-- wr	Assertion (h) synchronously writes memory(add) = dataToMem(31:0)


-- add	memory address
-- datToMem	memory write data


-- functBus	96-bit bus which can be connected to any threshold component signals, to be stored / viewed during threshold function execution
-- CSR1	to be completed
-- clk	clk signal
-- rst	rst signal

-- internal signal dictionary
-- NSYAdd	Y address std_logic_vector state signals
-- CSYAdd	Y address std_logic_vector state signals
-- NSXAdd	X address std_logic_vector state signals
-- CSXAdd	X address std_logic_vector state signals
-- BRAMByte	BRAM_dOut(CSXAdd*8+7 : CSXAdd*8)


-- NS 	Finite State Machine (FSM) next state and current state
-- CS 	Finite State Machine (FSM) next state and current state
-- NSThreshVec	thresholdVec std_logic_vector state signals


-- CSThreshVec	thresholdVec std_logic_vector state signals


-- threshVal	threshVal(7:0) = reg4x32_CSRA(31:24)

-- library declarations
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;


-- entity declaration
entity threshold is 
Port(
	ce : in std_logic;
	go : in std_logic;
	reg4x32_CSRA : in reg4x32_Array;
	reg4x32_CSRB : in reg4x32_Array;
	BRAM_dOut : in std_logic_vector(255 downto 0);
	active : out std_logic;
	wr : out std_logic;
	add : out std_logic_vector(7 downto 0);
	datToMem : out std_logic_vector(31 downto 0);
	functBus : out std_logic_vector(95 downto 0);
	CSR1 : in reg4x32_Array;
	clk : in std_logic;
	rst : in std_logic
);
end entity threshold;

architecture Combinational of threshold is
-- Internal signal declarations
type stateType is (idle, chkBRAM_Byte_GT_thresholdValue, wr_threshVec_to_reg32x32, write_status_to_reg4x32_CSRA0);
signal NSYAdd : std_logic_vector(4 downto 0);
signal CSYAdd : std_logic_vector(4 downto 0);
signal NSXAdd : std_logic_vector(4 downto 0);
signal CSXAdd : std_logic_vector(4 downto 0);
signal BRAMByte : std_logic_vector(7 downto 0);
signal NS  : stateType;
signal CS  : stateType;
signal NSThreshVec : std_logic_vector(31 downto 0);
signal CSThreshVec : std_logic_vector(31 downto 0);
signal threshVal : std_logic_vector(7 downto 0);

begin

NSAndOPDecode_p: process(go,reg4x32_CSRA,reg4x32_CSRB,CSYAdd,CSXAdd,BRAMByte,CS )
begin
	-- Complete the process if required
	active <= '0';-- default
	wr <= '0';-- default
	add <= all zeros;-- default
	datToMem <= all zeros;-- default
	functBus <= all zeros;-- default
	NSYAdd <= CSYAdd;-- default
	NSXAdd <= CSXAdd;-- default
	NS  <= CS ;-- default
	
	case CS  is
		when idle=>
			null;
		when  chkBRAM_Byte_GT_thresholdValue=>
			null;
		when  wr_threshVec_to_reg32x32=>
			null;
		when  write_status_to_reg4x32_CSRA0=>
			null;
		when others =>
			null;
	end case;
end process;

stateReg_p: process(clk,rst)
begin
	-- Complete the process if required
	if rst = '1' then
		CS  <= Idle;
		CSYAdd <= all zeros;
		CSXAdd <= all zeros;
		CSthreshVec <= all zeros;
	elsif rising_edge(clk) then
		CS  <= NS ;
		CSYAdd <= NSYAdd;
		CSXAdd <= NSXAdd;
		CSthreshVec <= NSthreshVec;
	end if;

end process;

asgn_add: add <= all zeros; -- Complete the concurrent statement if required

asgn_BRAMByte: BRAMByte <= all zeros; -- Complete the concurrent statement if required

end Combinational;