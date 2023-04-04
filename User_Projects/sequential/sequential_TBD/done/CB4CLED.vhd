-- Header (Description, Engineer, Date, Signal data dictionary)
-- Description: CB4CLED 4-bit cascadable up/down, loadable counter 
--              with chip enable, asynchronous rst
-- Engineer: Fearghal Morgan, National University of Ireland, Galway
-- Date: 7/12/2012
-- 
-- Signal data dictionary
--  clk			System clock strobe, rising edge active
--  rst			Synchronous reset signal. Assertion clears all registers, count=00
--  loadDat(3:0)	4-bit load data value
--  load			Assertion (H) synchronously loads count(3:0) register with loadDat(3:0) 
--              Load function does not require assertion of signal ce
--  ce			Assertion (H) enable synchronous count behaviour, if load is deasserted
--  up			Assertion (H) / deassertion (L) enables count up/down behaviour
--  count(3:0)	Counter value, changes synchronously on active (rising) clk edge
--  TC	Terminal count, asserted (H) when in up counter mode (up=1) and count(3:0)=0xF 
-- 					             or	 when in down counter mode (up=0) and count(3:0)=0
--  ceo	Chip enable output, asserted (H) when both ce and TC are asserted A
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity CB4CLED is
    Port ( clk 		: in STD_LOGIC;   
           rst 		: in STD_LOGIC;   
           loadDat	: in STD_LOGIC_VECTOR (3 downto 0); 
           load		: in STD_LOGIC;                
           ce 		: in STD_LOGIC;                
           up 		: in STD_LOGIC;                
           count	: out STD_LOGIC_VECTOR (3 downto 0);
           TC		: out STD_LOGIC;                    
           ceo		: out STD_LOGIC                     
           );
end CB4CLED;
architecture RTL of CB4CLED is
-- Internal signal declarations
signal NS : STD_LOGIC_VECTOR(3 downto 0); -- next state
signal CS : STD_LOGIC_VECTOR(3 downto 0); -- current state  
signal intTC : STD_LOGIC;                 -- internal signal (same as TC)
begin
-- Processes and concurrent statements 
NSDecode_i:       process(CS, loadDat, load, ce, up) -- generate NS
	begin
		NS <= CS; -- default assignment
		if load = '1' then
			NS <= loadDat;
		elsif ce = '1' then
			if up = '1' then NS <= std_logic_vector(unsigned(CS) + 1);
			else     	 	 NS <= std_logic_vector(unsigned(CS) - 1);
            end if;
		end if;
end process;
stateReg_i:       process(clk, rst) 				 -- generate CS()
begin
	if rst = '1' then           		
        CS <= (others => '0');
	elsif clk'event and clk = '1' then	
        CS <= NS;
	end if;
end process;
asgnCount_i:      count <= CS; 

OPDec_intTC_i: process (up, CS) 				     -- generate intTC
begin
	intTC <= '0'; -- default
	if    up = '1' and CS = "1111" then  
	   intTC <= '1';   
    elsif up = '0' and CS = "0000" then  
       intTC <= '1';   
    end if;
end process;
OPDec_asgnTC_i: TC    <= intTC; 					 -- generate TC
OPDec_ceo_i:    ceo   <= ce and intTC;               -- generate ceo
end RTL;