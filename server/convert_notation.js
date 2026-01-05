const express = require('express');
const { Builder, By, Key, until } = require('selenium-webdriver');
const fs = require('fs');
const cors = require('cors');

const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());


app.post('/descriptive-to-algebraic/', async (req, res) => {
    let notation = req.body.notation;
    if (!notation) {
        return res.status(400).send('Notation query parameter is required.');
    }
    for (let i = 0; i <= notation.length - 1; i++) {
        notation[i] = notation[i].split(",")
    }
    let algebraicNotation;
    try {
        algebraicNotation = await convertDescriptiveToAlgebraic(notation);
    } catch (error) {
        return res.status(500).send('Error occurred while converting notation.');
    }

    res.json({ algebraicNotation: algebraicNotation });
});

function convertDescriptiveToAlgebraic(descriptiveNotations) {
    return new Promise(async (resolve, reject) => {
        let driver = await new Builder().forBrowser('chrome').build();
        let combinedMoves = []
        let gamesObject = {}; // New object to hold the result

        let algebraicGames = []
        descriptiveNotations.forEach((notation, index) => {
            gamesObject["game" + (index + 1)] = algebraicGames[index] || "";
        });

        try {
            await driver.get('https://marianogappa.github.io/ostinato-examples/convert.html');
            for (let i = 0; i <= descriptiveNotations.length - 1; i++) {
                let game = descriptiveNotations[i].join(' ');

                let inputBox = await driver.findElement(By.id('input'));

                await inputBox.sendKeys(Key.COMMAND, 'a');  // Select all text (use Key.COMMAND on macOS)
                await inputBox.sendKeys(Key.BACK_SPACE);

                let outputBox = await driver.findElement(By.id('actions'));
                try {
                    await driver.wait(async () => {
                        let lineElements = await outputBox.findElements(By.className('line'));

                        if (lineElements.length === 1) {
                            let anchorTags = await lineElements[0].findElements(By.tagName('a'));
                            if (anchorTags.length >= 1) {
                                let anchorText = await anchorTags[0].getText();
                                return anchorText === '1/2-1/2'
                            }
                        }

                        return false;
                    }, 5000);
                }
                catch (error) {
                    console.error('Timeout while checking line elements', error);
                }

                await inputBox.sendKeys(game);

                outputBox = await driver.findElement(By.id('actions'));

                await driver.wait(async () => {
                    let lineElements = await outputBox.findElements(By.className('line'));

                    if (lineElements.length === 1) {
                        let anchorTags = await lineElements[0].findElements(By.tagName('a'));
                        if (anchorTags.length === 1 || anchorTags.length === 2) {
                            let anchorText = await anchorTags[0].getText();
                            return anchorText !== '1/2-1/2';
                        }
                    }

                    return lineElements.length === 0 || true;
                }, 5000);

                let lineElements = await outputBox.findElements(By.className('line'));

                let algebraicNotation = [];
                for (let line of lineElements) {
                    let anchorTags = await line.findElements(By.tagName('a'));

                    for (let anchor of anchorTags) {
                        let moveText = await anchor.getText();
                        algebraicNotation.push(moveText);
                    }
                }

                combinedMoves = {};
                for (let i = 0; i < algebraicNotation.length; i += 2) {
                    let moveNumber = Math.floor(i / 2) + 1;
                    let firstMove = algebraicNotation[i] || '';
                    let secondMove = algebraicNotation[i + 1] || '';
                    combinedMoves[moveNumber] = `${firstMove} ${secondMove}`.trim();
                }
                gamesObject['game' + (i + 1)] = combinedMoves
            }
        } finally {
            await driver.quit();
            resolve(gamesObject)
        }
    })
}


app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
