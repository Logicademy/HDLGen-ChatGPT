-- accumulator acc4 RTL model
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use ieee.numeric_std.all;

entity acc4 is
    Port ( clk    : in   STD_LOGIC;
	       rst    : in   STD_LOGIC;
	       cIn    : in   STD_LOGIC;
           ld     : in   STD_LOGIC;
           ldDat  : in   STD_LOGIC_VECTOR (3 downto 0);
           accIn  : in   STD_LOGIC_VECTOR (3 downto 0);
           ce     : in   STD_LOGIC;
           accOut : out  STD_LOGIC_VECTOR (3 downto 0);
           cOut   : out  STD_LOGIC
		  );
end acc4;

architecture RTL of acc4 is
signal intAdd : std_logic_vector (4 downto 0); -- 5 bit internal addition value 
signal CS     : std_logic_vector (3 downto 0); -- current state
signal NS     : std_logic_vector (3 downto 0); -- next state

begin

add5Conc:   intAdd <= std_logic_vector( unsigned('0' & CS) + unsigned('0' & accIn) + ("0000" & cIn) );
cOutAsgn: 	cOut   <= intAdd(4); 
accOutAsgn: accOut <= CS;

NSAndOPDecode_i: process (CS,  ld, ldDat, ce, intAdd)	
begin
 NS <= CS; -- default (no change)
 if ld = '1' then
	 NS <= ldDat;
 elsif ce = '1' then
	 NS <= intAdd(3 downto 0);
 end if;
end process;

synch_i: process (clk, rst)	
begin
 if rst = '1' then 
    CS <= (others => '0');
 elsif clk'event and clk = '1' then
	CS <= NS;   
 end if;
end process;

end RTL;