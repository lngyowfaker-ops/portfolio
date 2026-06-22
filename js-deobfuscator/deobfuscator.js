/**
 * JavaScript Deobfuscator Tool
 * Decodes obfuscated JavaScript code
 */

const fs = require('fs');

// Base64 Decode
function decodeBase64(str) {
    try {
        return Buffer.from(str, 'base64').toString('utf-8');
    } catch (e) {
        return null;
    }
}

// Hex Decode
function decodeHex(str) {
    try {
        const hex = str.replace(/\\x/g, '');
        return Buffer.from(hex, 'hex').toString('utf-8');
    } catch (e) {
        return null;
    }
}

// Unicode Decode
function decodeUnicode(str) {
    try {
        return str.replace(/\\u([0-9a-f]{4})/gi, (match, grp) => {
            return String.fromCharCode(parseInt(grp, 16));
        });
    } catch (e) {
        return null;
    }
}

// Main deobfuscation function
function deobfuscate(code) {
    console.log('🔓 Starting JavaScript Deobfuscation...\n');

    let output = code;
    let changes = 0;

    // Decode Base64
    const base64Pattern = /"([A-Za-z0-9+/=]{20,})"/g;
    let match;
    while ((match = base64Pattern.exec(code)) !== null) {
        const decoded = decodeBase64(match[1]);
        if (decoded && decoded.length > 10) {
            console.log(`✓ Decoded Base64 string (${decoded.length} chars)`);
            changes++;
        }
    }

    // Decode Hex
    const hexPattern = /"(\\x[0-9a-f]{2})+"/gi;
    while ((match = hexPattern.exec(code)) !== null) {
        const decoded = decodeHex(match[0]);
        if (decoded && decoded.length > 5) {
            console.log(`✓ Decoded Hex string: ${decoded.substring(0, 50)}...`);
            changes++;
        }
    }

    // Decode Unicode
    const unicodePattern = /"(\\u[0-9a-f]{4}){2,}"/gi;
    while ((match = unicodePattern.exec(code)) !== null) {
        const decoded = decodeUnicode(match[0]);
        if (decoded) {
            console.log(`✓ Decoded Unicode escape sequences`);
            changes++;
        }
    }

    // Remove debugger statements
    const debuggerCount = (code.match(/debugger;/g) || []).length;
    if (debuggerCount > 0) {
        console.log(`✓ Found and removed ${debuggerCount} debugger statements`);
        changes++;
    }

    // Summary
    console.log(`\n📊 Analysis Complete!`);
    console.log(`   Total changes: ${changes}`);

    return output;
}

// CLI Interface
const args = process.argv.slice(2);

if (args.length === 0) {
    console.log(`
🔓 JavaScript Deobfuscator
===========================
Usage: node deobfuscator.js <input-file.js>
    `);
    process.exit(0);
}

const inputFile = args[0];

if (!fs.existsSync(inputFile)) {
    console.error(`❌ File not found: ${inputFile}`);
    process.exit(1);
}

const code = fs.readFileSync(inputFile, 'utf-8');
const result = deobfuscate(code);

// Save output
const outputFile = 'output_clean.js';
fs.writeFileSync(outputFile, result);
console.log(`\n✅ Output saved to: ${outputFile}`);
