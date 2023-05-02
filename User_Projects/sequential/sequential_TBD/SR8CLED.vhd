-- Description: SR8CLED: 8-bit loadable/left/right shift register, with chip enable and asynchronous rst 
-- Authors: Fearghal Morgan
-- Date: 18/5/2015
-- Change History: Initial version
-- CS'left VHDL attribute for std_logic_vector(7 downto 0) provides the leftmost bit index, i.e, 7 here.
-- Use this VHDL attribute in the VHDL model 

-- Signal dictionary
-- clk 		 system clock strobe. 
-- rst 		 assertion (high) asynchronously clears all registers
-- load 	 assertion (high) synchronously loads the register with value loadDat. load has priority over signal ce 
-- loadDat 	 load data word (8 bits) 
-- ce 		 assertion (high) enables the shift register to synchronously shift left or right, when load is deasserted
-- shiftLeft assertion/deassertion (high/low) enables shift left/right, with serInLSB/serInMSB shifted into shift register bit LSB/MSB
-- serInLSB  one bit data shifted into register least significant bit, on a left shift (shiftLeft asserted)
-- serInMSB  one bit data shifted into register most significant bit,  on a right shift  (shiftLeft deasserted)
-- SRegOut 	 8-bit shift register output

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity SR8CLED is
    Port ( clk 		: in STD_LOGIC;                     
           rst 		: in STD_LOGIC;                     
           load 	: in STD_LOGIC;                     
           loadDat 	: in STD_LOGIC_vector(7 downto 0);  
           ce 		: in STD_LOGIC;                     
           shiftLeft: in STD_LOGIC;                     
           serInLSB : in STD_LOGIC;                     
           serInMSB : in STD_LOGIC;                     
           SRegOut 	: out STD_LOGIC_VECTOR(7 downto 0)  
         );
end SR8CLED;

architecture RTL of SR8CLED is
-- Signal declaration for 2-process HDL description
-- Signal CS used to generate NS, since SRegOut (defined as output signal) cannot be used on the right hand side of an assignment
signal NS : STD_LOGIC_VECTOR(7 downto 0); 
signal CS : STD_LOGIC_VECTOR(7 downto 0);  

begin

NSDecode_i: process (load, loadDat, ce, CS, shiftLeft, serInLSB, serInMSB)
begin
	NS <= CS; -- default assignment
    if load = '1' then
  		NS <= loadDat;
    elsif ce = '1' then 
   		if shiftLeft = '1' then
   			NS <= CS( (CS'left-1) downto 0 ) & serInLSB; -- (CS'left-1) = 6 here
		else
			NS <= serInMSB & CS( (CS'left) downto 1 );    
		end if;
	end if;
end process;

stateReg_i: process(clk, rst)
begin
  if rst = '1' then
    CS  <= (others => '0'); 
  elsif clk'event and clk = '1' then
    CS  <= NS; 
  end if;
end process;

asgnSRegOut_i: SRegOut <= CS; 

end RTL;