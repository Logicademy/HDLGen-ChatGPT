-- Package
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
package arrayPackage is
type array3x12 is array(3 downto 0) of std_logic_vector(12 downto 0);
type array3x12_signed is array(3 downto 0) of signed(12 downto 0);
type array3x12_unsigned is array(3 downto 0) of unsigned(12 downto 0);


end arrayPackage;
package body arrayPackage is
end arrayPackage;

