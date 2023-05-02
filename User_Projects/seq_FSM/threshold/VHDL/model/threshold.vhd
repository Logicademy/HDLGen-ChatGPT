-- Header Section
-- Component Name : threshold
-- Title          : Generate a 32-x32-bit threshold array from 32x32-byte source (BRAM) data array

-- Description
-- Generate a 32-x32-bit threshold array from 
-- - 32x32-byte source (BRAM) data array
-- - threshVal(7:0)
-- 
-- Result bit is asserted if souce byte >= threshVal

-- Author(s)      : Fearghal Morgan
-- Company        : University of Galway
-- Email          : fearghal.morgan@universityofgalway.ie
-- Date           : 13/01/2023

-- entity signal dictionary
-- clk	clk signal
-- rst	rst signal
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
use work.MainPackage.all;

entity threshold is 
Port(
	clk : in std_logic;
	rst : in std_logic;
	ce : in std_logic;
	go : in std_logic;
	reg4x32_CSRA : in reg4x32_Array;
	reg4x32_CSRB : in reg4x32_Array;
	BRAM_dOut : in std_logic_vector(255 downto 0);
	active : out std_logic;
	wr : out std_logic;
	add : out std_logic_vector(7 downto 0);
	datToMem : out std_logic_vector(31 downto 0);
	functBus : out std_logic_vector(95 downto 0)
);
end entity threshold;

architecture RTL of threshold is
-- Internal signal declarations
type stateType is (idle, chkBRAM_Byte_GT_thresholdValue, wr_threshVec_to_reg32x32, write_status_to_reg4x32_CSRA0);
signal NS  : stateType;
signal CS  : stateType;
signal NSYAdd : std_logic_vector(4 downto 0);
signal CSYAdd : std_logic_vector(4 downto 0);
signal NSXAdd : std_logic_vector(4 downto 0);
signal BRAMByte : std_logic_vector(7 downto 0);
signal NSThreshVec : std_logic_vector(31 downto 0);
signal CSThreshVec : std_logic_vector(31 downto 0);
signal CSXAdd : std_logic_vector(4 downto 0);
signal threshVal : std_logic_vector(7 downto 0);

begin

genBRAMByte: BRAMByte <= BRAM_dOut(to_integer(unsigned(CSXAdd))*8+7 downto to_integer(unsigned(CSXAdd))*8);

asgn_ThreshVal: threshVal <= reg4x32_CSRA(0)(31 downto 24);

NSAndOPDecode_p: process(CS, go,reg4x32_CSRA,reg4x32_CSRB,CSYAdd,CSXAdd,CSthreshVec,threshVal,BRAMByte)
begin
	-- Complete the process
	NS  <= CS;
	active <= '1';
	NSYAdd <= CSYAdd;
	NSXAdd <= CSXAdd;
	NSthreshVec <= CSthreshVec;
	wr  <= '0';
    add <= "010" & CSYAdd; -- address 32 x 256-bit BRAM
	datToMem <= CSThreshVec;
	
	case CS  is
		when idle=>
			NSThreshVec     <= (others => '0');    
			NSYAdd          <= (others => '0');    
			NSXAdd          <= (others => '0');    
            if go = '1' then 
				NS 	        <= chkBRAM_Byte_GT_thresholdValue;
			else
				active      <= '0';  
			end if;

		when  chkBRAM_Byte_GT_thresholdValue=>
			if unsigned(BRAMByte) > unsigned(threshVal)  then 
				NSThreshVec( to_integer(unsigned(CSXAdd)) ) <= '1';-- set single bit of vector
			end if;
			if unsigned(CSXAdd) = "11111" then          		   -- = 31 => final BRAMByte
				NS      <= wr_threshVec_to_reg32x32;   	           -- final threshVec value is ready in wr_threshVec_to_reg32x32 state
			end if;
			NSXAdd      <= std_logic_vector(unsigned(CSXAdd) + 1); -- increment XAdd counter

		when  wr_threshVec_to_reg32x32=>
			wr          <= '1';                                    
            add         <= "001" & CSYAdd;                         -- resultMem address
   	  	    NSThreshVec <= (others => '0');                        -- clear  
		    NSYAdd      <= std_logic_vector(unsigned(CSYAdd) + 1); -- increment YAdd counter
			if unsigned(CSYAdd) < "11111" then                     -- loop 
			    NS      <= chkBRAM_Byte_GT_thresholdValue;         -- process next BRAM word 
            else
				NS      <= write_status_to_reg4x32_CSRA0;          -- exit loop if at final BRAM word (YAdd = 31)
			end if;

		when  write_status_to_reg4x32_CSRA0=>
			wr          <= '1';
			add         <= X"00";                                  -- address CSRA(0) 
		    datToMem    <= reg4x32_CSRA(0)(31 downto 2) & "10"; 
		    NS          <= idle;

		when others =>
			null;
	end case;
end process;

stateReg_p: process(clk,rst)
begin
	-- Complete the process
	if rst = '1' then
		CS  <= idle;
		CSYAdd <= (others => '0');
		CSXAdd <= (others => '0');
		CSThreshVec <= (others => '0');
	elsif rising_edge(clk) then
	    if ce = '1' then
    	   CS  <= NS ;
	   	   CSYAdd <= NSYAdd;
		   CSXAdd <= NSXAdd;
		   CSThreshVec <= NSthreshVec;
		end if;
	end if;

end process;

asgn_functBus: functBus <= (others => '0');

end RTL;