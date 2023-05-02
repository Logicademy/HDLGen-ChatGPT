-- Authors: Fearghal Morgan
-- Description: decode 2 bits to 4 bits
-- Engineer: Fearghal Morgan
-- viciLogic 
-- Date: 12/9/2016
--
-- dec2To4In(1:0)   input  2 bit data
-- dec2To4Out(1:0)  decoded output 4 bit data

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL; -- support arithmetic functions

entity dec2To4 is
    Port ( dec2To4In  : in  std_logic_vector(1 downto 0); 
           dec2To4Out : out std_logic_vector(3 downto 0)  
         );         
end dec2To4;

architecture comb of dec2To4 is
begin

process (dec2To4In)
begin
	dec2To4Out <= (others => '0');  
	dec2To4Out( to_integer(unsigned(dec2To4In)) ) <= '1';
end  process;

end comb;


-- signal integerDec2To4In : integer range 0 to 15; -- internal signal, used in some of the VHDL models
-- integerDec2To4In <= TO_INTEGER(unsigned(dec2To4In)); -- assign integer signal with integer-converted value of dec2To4In(1:0)

-- -- ==== Using case statement (in process) ====
-- dec2To4_case_i1: process (dec2To4In)
-- begin
  -- dec2To4Out <= (others => '0'); -- default
  -- case dec2To4In is 
      -- when "00" => dec2To4Out <= "0001";  
      -- when "01" => dec2To4Out <= "0010"; 
      -- when "10" => dec2To4Out <= "0100"; 
      -- when "11" => dec2To4Out <= "1000";  
      -- when others => null; 
  -- end case;
-- end process;


--decoder_case_i2: process (integerDec2To4In)  
--begin
--  dec2To4Out <= (others => '0'); -- default assignment (all deasserted)
--  case integerDec2To4In is 
--      when 0    => dec2To4Out(0) <= '1'; -- assert individual bit of dec2To4Out(3:0)
--      when 1    => dec2To4Out(1) <= '1'; 
--      when 2    => dec2To4Out(2) <= '1'; 
--      when 3    => dec2To4Out(3) <= '1'; 
--      when others => null; 
--  end case;
--end process;
--end comb;


---- ==== Using concurrent statement (process is not required) ====
--dec2To4_case_i: dec2To4Out <= "0001" when dec2To4In = "00" else -- use indentation to help presentation clarity
--                              "0010" when dec2To4In = "01" else 
--                              "0100" when dec2To4In = "10" else 
--                              "1000" when dec2To4In = "11";                              
--end comb;

                              
--dec2To4_conc_i: dec2To4Out <= "0001" when TO_INTEGER(unsigned(dec2To4In)) = 0 else -- use indentation to help presentation clarity
--                              "0010" when TO_INTEGER(unsigned(dec2To4In)) = 1 else 
--                              "0100" when TO_INTEGER(unsigned(dec2To4In)) = 2 else 
--                              "1000" when TO_INTEGER(unsigned(dec2To4In)) = 3;
--end comb;


--decoder_conc_i: dec2To4Out <= "0001" when integerDec2To4In = 0 else -- use indentation to help presentation clarity
--                              "0010" when integerDec2To4In = 1 else 
--                              "0100" when integerDec2To4In = 2 else 
--                              "1000" when integerDec2To4In = 3;
--end comb;


---- ==== Using if statement (in process) ====
--decoder_if_i1: process (integerDec2To4In)  
--begin
--  dec2To4Out <= (others => '0'); -- default assignment (all deasserted)
--  if    integerDec2To4In = 0 then dec2To4Out(0) <= '1'; -- assert individual bit of dec2To4Out(3:0)
--  elsif integerDec2To4In = 1 then dec2To4Out(1) <= '1';  
--  elsif integerDec2To4In = 2 then dec2To4Out(2) <= '1';  
--  elsif integerDec2To4In = 3 then dec2To4Out(3) <= '1';  
--  end if; 
--end process;
--end comb;


--decoder_if_i2: process (integerDec2To4In)  
--begin
--  dec2To4Out <= "0001"; -- default assignment, when integerDec2To4In = 0
--  if    integerDec2To4In = 1 then dec2To4Out <= "0010";  
--  elsif integerDec2To4In = 2 then dec2To4Out <= "0100";  
--  elsif integerDec2To4In = 3 then dec2To4Out <= "1000";  
--  end if; 
--end process;
--end comb;
