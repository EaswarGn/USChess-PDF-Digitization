
let descriptiveNotations = [
    ["1. P-K4 P-K4",
        "2. N-KB3 N-QB3",
        "3. B-B4 B-B4",
        "4. N-B3 N-B3",
        "5. O-O O-O",
        "6. R-K1 P-Q3",
        "7. P-Q4 PxP",
        "8. NxP N-K5",
        "9. BxN BxB",
        "10. NxB QxN"],
    [
        "1. P-K4 P-K4",
        "2. N-KB3 N-QB3",
        "3. B-B4 B-B4",
        "4. N-B3 N-B3",
        "5. O-O O-O",
    ]
];

//combine each game of descriptive notations into a single string to pass to the server,
//add a space between each move
for (let i = 0; i <= descriptiveNotations.length - 1; i++) {
    descriptiveNotations[i] = descriptiveNotations[i].join(' ');
}