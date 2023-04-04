-- Component: reg4x32
-- Engineer: Fearghal Morgan, National University of Ireland, Galway
-- Date: 26/1/2021

-- m = 2
-- n = number of words = 2**m
-- register array reg(n-1:0)(31:0)  

--Description
-- n x 32-bit register array
-- ld0   assertion (h) clears all array bits 
-- we    assertion (h) stores register array(add)(31:0) = dIn(31:0) 
-- Combinationally outputs all register data array values on reg(n-1:0)(31:0)
-- dOut(31:0) combinationally = register(add)
-- rst assertion asynchronously clears all registers

-- Signal dictionary
--  clk				   system strobe, rising edge asserted
--  rst				   assertion (h) asynchronously clears all registers

-- 	ld0     		   assertion (h) clears all array bits 
--  we 				   assertion (h) synchronously writes dIn(31:0) to reg(add)
--  add(m-1:0)		   m-1 bit address, addressing one of the registers 
--  dIn(31:0)		   32-bit data to be written to reg(add) 
--  reg(n-1:0)(31:0)   n x 32-bit register array 
--  dOut(31:0)	       = array(add) combinational output 

-- Internal signal dictionary
--  XX_NS			    Next state signal    (n x 32-bit array) 
--  XX_CS			   Current state signal (n x 32-bit array). Output signal reg = XX_CS.

library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.numeric_std.all;
use work.arrayPackage.all;

entity reg4x32_CSRB_c is
    Port ( clk       : in std_logic;   
           rst       : in std_logic;
           ld0       : in std_logic;   		   
           
           we        : in std_logic;  
	       add       : in std_logic_vector(1 downto 0);
	       dIn3DT1   : in std_logic_vector(95 downto 0);	  
	       dIn       : in std_logic_vector(31 downto 0);	  
           
           reg       : out array4x32;
           dOut      : out std_logic_vector(31 downto 0)
 		 );
end reg4x32_CSRB_c;

architecture RTL of reg4x32_CSRB_c is
signal XX_NS : array4x32;	  
signal XX_CS : array4x32;	

begin

NSDecode_i: process(XX_CS, ld0, we, add, dIn, dIn3DT1)
begin
	XX_NS <= XX_CS; -- defaults
    if ld0 = '1' then 
    	XX_NS <= ( others => (others => '0') );   
    elsif we = '1' then 
     	XX_NS( to_integer(unsigned(add)) ) <= dIn; -- default write dIn to addressed register 
        if XX_CS(0)(3) = '1' then                  -- if CS(0)(3) = 1, wrtie functBus(95:0) to XX_CS(3:1), on every active clk edge
	       XX_NS(3) <= dIn3DT1(95 downto 64); 
	       XX_NS(2) <= dIn3DT1(63 downto 32); 
	       XX_NS(1) <= dIn3DT1(31 downto  0); 
      	end if;
	end if;
end process;

stateReg_i: process(clk, rst) 
begin
	if rst = '1' then 
		XX_CS <= (others => (others => '0'));
	elsif (clk'event and clk = '1') then
		XX_CS <= XX_NS;
	end if;	 
end process;

asgnCSR_i:   reg <= XX_CS; 

genDOut_i:   dOut <= XX_CS( to_integer(unsigned(add)) );

end RTL;