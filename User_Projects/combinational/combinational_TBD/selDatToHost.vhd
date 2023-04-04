-- Description: selDatToHost
-- Engineer: Fearghal Morgan, National University of Ireland, Galway
-- Date: 7/2/2021

-- Description
-- decodes add(7:5) to select memory component data output on datToHost 

-- signal dictionary
--  selSlice 	 			   3-bit memAdd(10:9) selecting 32-bit data slice 
--                             000 => word 0 bits 31:0, 111 => word 7 bits 255:224
--  reg4x32_CSRA_dOut          addressed 32-bit data from 4x32-bit register memory (CSRA)
--  XX_intBRAM32x256_dOut      addressed 32-bit data from 32 x 256-bit BRAM source memory array  
--  XX_intReg32x32_dOut        addressed 32-bit data from 32x32-bit register memory 
--  reg4x32_CSRB_dOut          addressed 32-bit data from 4x32-bit register memory (CSRB)
--  datToHost                  32-bit data to host 

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
use work.arrayPackage.all;

entity selDatToHost is
    Port ( memAdd       	   : in  std_logic_vector( 10 downto 0);
		   XX_intBRAM32x256_dOut : in  std_logic_vector(255 downto 0);
		   XX_intReg32x32_dOut : in  std_logic_vector( 31 downto 0);
		   reg4x32_CSRA_dOut   : in  std_logic_vector( 31 downto 0);
		   reg4x32_CSRB_dOut   : in  std_logic_vector( 31 downto 0);
		   datToHost           : out std_logic_vector( 31 downto 0)		   
 		 );
end selDatToHost;

architecture comb of selDatToHost is
constant BRAM_add_7DT5          : std_logic_vector(2 downto 0) := "001";
constant reg32x32_add_7DT5      : std_logic_vector(2 downto 0) := "010";
constant reg4x32_CSRA_add_7DT5  : std_logic_vector(2 downto 0) := "000";
constant reg4x32_CSRB_add_7DT5  : std_logic_vector(2 downto 0) := "011";
signal   wordIndex              : integer range 0 to 7; 

-- signals used in vicilogic -- could be omitted from model

begin

-- Select the 32-bit slice of XX_intBRAM32x256_dOut 256 = 8 x 32-bit words 
asgnIndex_i: wordIndex <= to_integer( unsigned(memAdd(10 downto 8)) );

asgnDatToHost_i: process (memAdd, wordIndex, XX_intBRAM32x256_dOut, XX_intReg32x32_dOut, reg4x32_CSRA_dOut, reg4x32_CSRB_dOut)
begin 
  datToHost    <= (others => '0'); -- default
  if memAdd(7 downto 5) = BRAM_add_7DT5 then    
     datToHost <= XX_intBRAM32x256_dOut( (32*wordIndex + 31) downto (32*wordIndex) );
  elsif memAdd(7 downto 5) = reg32x32_add_7DT5 then  
     datToHost <= XX_intReg32x32_dOut;
  elsif memAdd(7 downto 5) = reg4x32_CSRA_add_7DT5 then
     datToHost <= reg4x32_CSRA_dOut; 
  elsif memAdd(7 downto 5) = reg4x32_CSRB_add_7DT5 then   
     datToHost <= reg4x32_CSRB_dOut;
  end if;
end process;

end comb;