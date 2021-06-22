# Matrix_Encoding
An encoding and decoding algorithm using arbitrary sized matrix multiplication. 

This was written in python 3.6, and I was still failry inexperienced with the language. 
It is also important to note that I designed this to be easily tested by splitting code into small functions. Alas, I did not get to writing said tests. 

This encoding algorithm performs the following steps: 
1. Converts the input test to a numerical matrix. 
2. Generates a key matrix of a random size
3. Multiply these the key matrix by the numerical input to get the first level of encoding. 
4. Fold the two matrices together by distributing the key list evenly throughout the encoded matrix list. 
5. Multiply that new larger list by the static master key to get the second level of encription. 

At this point, it would be exceedingly difficult to divine what the output numbers mean without some knowledge of how this program works. 

The decode function performs these steps in reverse. After removing the second level of encoding by multiplying the input numbers by the inverted master key, 
the algorithm will separate out the originally generated key and the original values, then multiply the values by the inverse of the key. 

NOTE: There is one small problem with this program in its current state. 
Sometimes, the matrix multiplication will yeild massive values which end up losing precision due to their size. 
I would need to find some way to increase float precision for this application to work in all cases. 
This problem gets worse if the generated matrix key has large values (I put constraints on this to reduce the possibility, but it still happens.)
If it fails, simply try again. If it still doesn't work, try entering a smaller string. 
