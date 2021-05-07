=== Testing Account ===
user id: admin
password: Ab123456
Remember me toggle is checked by default so you do not need to enter your password every time you test.
A bank card with number 1234567890123456 is registered.
The card is connected to admin account.

=== The function of each directory ===

./receipts
This folder act as a simulated printer.
It contains all the receipts that are supposed to be printed.
These files are all image files with png extension.

./res
This folder include all the resources that are required to run the program.
It contains all the information about purchasable items.
It also contains all the icons and images that improves with the interface.

./save
This folder contains the record of accounts, purchases etc.
You may remove all files, the software can handle FileNotFound.
However, you will lose all the existing accounts, purchase records etc.
There are two kinds of files.
- Pickle files (*.p)
    They are binary files that are NOT supposed to be opened using text editors.
    You must NOT change the content in these files.
- Text files (*.txt)
    This kind of file is safe to open.
