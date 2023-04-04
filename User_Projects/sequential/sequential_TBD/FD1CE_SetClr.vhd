-- Description: -- FD1CE_SetClr 1-bit set/clr register with asynchronous reset 
-- Engineer: Fearghal Morgan
-- Date: 07/10/2018
-- Change History: Initial version

-- Signal data dictionary
-- clk		clk strobe, rising edge active.
-- rst 		assertion (high) asynchronous clears register.
-- ce	    assertion (h) enable the register operation  
-- set	    assertion (h) synchronously asserts   register Q output. Has priority over clr signal. 
-- clr      assertion (h) synchronously deasserts register Q output.
-- Q	    register data out

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;  
use IEEE.numeric_std.ALL; 

entity FD1CE_SetClr is
    Port ( clk 		: in STD_LOGIC;  
           rst 		: in STD_LOGIC;  
           ce	    : in STD_LOGIC;  
           set	    : in STD_LOGIC;  
           clr	    : in STD_LOGIC;  
           Q	    : out STD_LOGIC  
		  );
end FD1CE_SetClr;

architecture RTL of FD1CE_SetClr is
signal NS : std_logic; -- next state  
signal CS : std_logic; -- current state 

begin

NSDecode_i: process (CS, ce, set, clr)
begin
    NS <= CS; -- default assignment     
    if ce = '1' then 
        if set = '1' then
            NS <= '1'; 
        elsif clr = '1' then
            NS <= '0'; 
        end if;
    end if;
end process;

stateReg_i: process(clk, rst)
begin
	if rst = '1' then -- asynch rst
		CS <= '0';    -- clear CS
	elsif rising_edge(clk) then  
		CS <= NS;
	end if;
end process;

asgnQ_i: Q <= CS;

end RTL;