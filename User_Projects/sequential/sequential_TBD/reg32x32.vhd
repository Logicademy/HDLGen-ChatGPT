-- reg32x32 VHDL model, with synchronous ld0 and ce control
-- Created : Oct 2019
-- Engineer: Fearghal Morgan, National University of Ireland, Galway
-- Date: 10 Oct 2019

-- Description
-- 32 x 32-bit register array
-- If ld0 is asserted 
--   synchronously clears all register words 
-- elsif ce is asserted 
--   If we asserted, synchronously stores data in register (add)(31:0) = dIn(31:0) 
-- rst assertion   asynchronously clears all registers

-- Signal dictionary
--  clk				   system strobe, rising edge asserted
--  rst				   assertion (h) asynchronously clears all registers

-- 	ld0     		   assertion (h) clears all array bits 
--  we 				   assertion (h) synchronously writes dIn(31:0) to reg(add)
--  add(m-1:0)		   m-1 bit address, addressing one of the registers 
--  dIn(31:0)		   32-bit data to be written to CSR(add) 
--  reg(n-1:0)(31:0)   n x 32-bit register array 
--  dOut(31:0)	       = array(add) combinational output 

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
use work.arrayPackage.all;

entity reg32x32 is
    Port ( clk    : in std_logic;   
           rst    : in std_logic;
           ld0    : in std_logic;     
           we     : in std_logic;    				       
	       add    : in std_logic_vector(4 downto 0);	  
	       dIn    : in std_logic_vector(31 downto 0);	  
           reg    : out array32x32;
           dOut   : out std_logic_vector(31 downto 0)
 		 );
end reg32x32;

architecture RTL of reg32x32 is
signal XX_NS : array32x32; -- internal next state signal
signal CS : array32x32; -- internal current state signal

begin

NSDecode_i: process(CS, ld0, we, add, dIn)
begin
	XX_NS <= CS; -- default

	if ld0 = '1' then 
	  XX_NS <= (others => (others => '0')); 
	elsif we = '1' then 
   	  XX_NS( to_integer(unsigned(add)) ) <= dIn;
	end if;
end process;

stateReg_i: process(clk, rst)
begin
	if rst = '1' then 
		CS <= (others => (others => '0'));
	elsif (clk'event and clk = '1') then
		CS <= XX_NS;
	end if;	 
end process;

asgnCSR_i:  reg  <= CS; 

asgnDOut_i: dOut <= CS( to_integer(unsigned(add)) );

end RTL;