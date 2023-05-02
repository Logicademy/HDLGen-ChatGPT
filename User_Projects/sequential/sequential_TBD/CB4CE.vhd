-- Description: CB4CE 4-bit cascadable up counter with clock enable and asynchronous rst
-- Outputs: count(3:0), terminal count (TC) and clock enable out (ceo)
-- 2 process model, stateReg and NSAndOPDecode.
-- NSAndOPDecode divided into two processes, NSDecode and OPDecode. Also includes concurrent assignment to ceo o/p signal.
-- Engineer: Fearghal Morgan
-- viciLogic 
-- Date: 7/12/2012
-- Change History: Initial version

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity CB4CE is
 Port (clk  : in  STD_LOGIC;                   -- clk strobe, rising edge active
       rst  : in  STD_LOGIC;                   -- asynch, high asserted rst        
       ce	: in STD_LOGIC;                    -- chip enable, asserted high
       count: out STD_LOGIC_VECTOR(3 downto 0);-- count output 
       TC 	: out STD_LOGIC;                   -- asserted (h) when count=Fh
	   ceo 	: out STD_LOGIC                    -- asserted (h) when count=Fh and ce asserted
      );
end CB4CE;

architecture RTL of CB4CE is
signal NS : STD_LOGIC_VECTOR(3 downto 0); -- next state
signal CS : STD_LOGIC_VECTOR(3 downto 0); -- current state  
signal intTC : STD_LOGIC;                 -- internal signal (same as TC)

begin

NSDecode_i: process (CS, ce)
begin
  NS <= CS;                 -- default assignment
  if ce = '1' then          -- increment unsigned vector. 
                            -- Convert result to std_logic_vector(3 downto 0) 
	NS <= std_logic_vector(unsigned(CS) + "0001"); -- if "1111", std_logic_vector (slv) + 1 automatically rolls over to 0
  end if;
end process;

OPDecode_TC_i: process (CS) -- Use intTC internal signal since cannot 
                            -- use TC on right hand side of ceo assignment 
begin
  intTC <= '0';             -- default
  if CS = "1111" then 
	intTC <= '1'; 
  end if;
end process;
OPDecode_ceo_i: ceo <= ce and intTC;
OPDecode_asgnTC_i: TC  <= intTC; -- assign output signal


stateReg_i: process(clk, rst) 
begin
 if rst = '1' then                        -- async rst
   CS <= (others => '0');                 -- clear CS. Could use CS <= "0000";
 elsif rising_edge(clk) then  
   CS <= NS;
 end if;
end process;

asgnCount_i: count <= std_logic_vector(unsigned(CS)); -- convert to slv 

end RTL;
