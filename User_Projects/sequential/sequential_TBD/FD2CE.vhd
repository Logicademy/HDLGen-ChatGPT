-- Engineer: Fearghal Morgan
-- viciLogic 
-- Create Date: 13/09/2015 
-- FD2CE 2-bit register with asynchronous reset and chip enable

-- Signal data dictionary
-- clk 		: in STD_LOGIC; 					-- clk strobe, rising edge active
-- rst 		: in STD_LOGIC; 					-- asynch, high asserted rst        
-- ce	    : in STD_LOGIC; 					-- chip enable, asserted high
-- D	    : in STD_LOGIC_VECTOR(1 downto 0); 	-- register data in 

-- Q	    : out STD_LOGIC_VECTOR(1 downto 0) 	-- register data out

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use ieee.numeric_std.all;

entity FD2CE is
 Port ( clk : in STD_LOGIC;
        rst : in STD_LOGIC;           
        ce	: in STD_LOGIC;  
        D	: in STD_LOGIC_VECTOR(1 downto 0);  
        Q   : out STD_LOGIC_VECTOR(1 downto 0)
      );
end FD2CE;

architecture RTL of FD2CE is
-- declare internal signals
signal NS : STD_LOGIC_vector(1 downto 0);
signal CS : STD_LOGIC_vector(1 downto 0);

begin

NSDecode_i: process (CS, ce, D)
begin
    NS <= CS; -- default assignment     
    if ce = '1' then
        NS <= D; 
    end if;
end process;

stateReg_i: process(clk, rst) 
begin
	if rst = '1' then
		CS <= (others => '0');
	elsif clk'event and clk = '1' then
		CS <= NS;
	end if;
end process;

asgn_Q: Q <= CS;

end RTL;
