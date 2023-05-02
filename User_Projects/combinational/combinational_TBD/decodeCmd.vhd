-- decodeCmd VHDL model 
-- Engineer: Fearghal Morgan, National University of Ireland, Galway
-- Date: Sept 2022

-- Description
-- generates go signal pulse to function component

-- Signal dictionary
--   clk
--   rst

--   reg4x32_CSRA_0
--     reg4x32_CSRA_0(15:11) is function select control
--	   case functSel is 
--		  when "00000" =>  go <= 0; -- maxMinPixelInBRAMWord0
--		  when "00001" =>  go <= 1; -- maxMinPixelInBRAM
--		  when "00010" =>  go <= 2; -- threshold
--		  when "00011" =>  go <= 3; -- Sobel
--		  when others  => null;
--	   end case;			
--   reg4x32_CSRA_0(0)(0)
--    =  0 configures host as master
--    =  1 configures FPGA as master

--  go  32-bit vector asserted for one clk perio to activate selected DSP function  

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
use work.arrayPackage.all;

entity decodeCmd is 
    Port (clk  	           : in  STD_LOGIC;
          rst              : in  STD_LOGIC;		  
          reg4x32_CSRA_0   : in  std_logic_vector(31 downto 0);
          go               : out std_logic_vector(31 downto 0)
          );	
end decodeCmd;

architecture RTL of decodeCmd is
type stateType is (waitFor1, waitFor0); -- declare enumerated state type
signal CS, NS    : stateType;     			-- declare state signals 
signal sw        : std_logic;
signal aShot     : std_logic;

signal functSel  : std_logic_vector(4 downto 0);
signal enGoPulse : std_logic;

begin

--enGo_i: singleShot 
--Port map (clk   => clk, 
--          rst   => rst,  
--          sw    => reg4x32_CSRA_0(0), 
--          aShot	=> enGoPulse
--	  ); 

asgnSw_i: sw <= reg4x32_CSRA_0(0);

-- Synchronous process defining state value
stateReg_i: process (clk, rst)
begin
  if rst = '1' then 		
    CS <= waitFor1;		
  elsif clk'event and clk = '1' then 
    CS <= NS;
  end if;
end process; 

-- Next state and o/p decode process
NSAndOPDec_i: process (CS, sw)
begin
   aShot <= '0';    				-- default assignment of process o/p signals 
   NS 	 <= CS; 				
   
   case CS is
		when waitFor1 => 			-- move to state waitFor0 if sw = '1'. 
									-- Otherwise no change from default values
			if sw = '1' then 
				aShot <= '1';    	-- combinationally assert unregistered o/p
				NS <= waitFor0;
			end if;
		when waitFor0 => 			-- remain in state waitFor0 unless sw = '0'. 
								    -- Otherwise no change from default values
			if sw = '0' then 
				NS <= waitFor1;
			end if;
		when others => 
			null;           		-- do nothing since default assignments apply
   end case;
end process; 
      
asgn_enGoPulse_i: enGoPulse <= aShot;


functSel_i: functSel <= reg4x32_CSRA_0(15 downto 11);

genGoIndex_i: process (enGoPulse, functSel)
begin
	go <= (others => '0');
	if enGoPulse = '1' then
		go( to_integer(unsigned(functSel)) ) <= '1';
	end if;
end process;

end RTL;