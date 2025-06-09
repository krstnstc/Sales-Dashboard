const fs = require('fs');
const { execSync } = require('child_process');
const sharp = require('sharp');

// Ensure the favicon directory exists
const faviconDir = './favicon';
if (!fs.existsSync(faviconDir)) {
  fs.mkdirSync(faviconDir, { recursive: true });
}

// Function to generate favicon files
async function generateFavicons() {
  try {
    console.log('🔄 Generating favicons...');
    
    // Read the SVG file
    const svg = fs.readFileSync(`${faviconDir}/favicon.svg`);
    
    // Generate favicon.ico (16x16, 32x32, 48x48)
    await sharp(svg)
      .resize(64, 64)
      .toFile(`${faviconDir}/favicon.ico`);
    
    // Generate favicon-16x16.png
    await sharp(svg)
      .resize(16, 16)
      .toFile(`${faviconDir}/favicon-16x16.png`);
    
    // Generate favicon-32x32.png
    await sharp(svg)
      .resize(32, 32)
      .toFile(`${faviconDir}/favicon-32x32.png`);
    
    // Generate apple-touch-icon.png (180x180)
    await sharp(svg)
      .resize(180, 180)
      .toFile(`${faviconDir}/apple-touch-icon.png`);
    
    // Generate android-chrome-192x192.png
    await sharp(svg)
      .resize(192, 192)
      .toFile(`${faviconDir}/android-chrome-192x192.png`);
    
    // Generate android-chrome-512x512.png
    await sharp(svg)
      .resize(512, 512)
      .toFile(`${faviconDir}/android-chrome-512x512.png`);
    
    console.log('✅ Favicons generated successfully!');
  } catch (error) {
    console.error('❌ Error generating favicons:', error);
    process.exit(1);
  }
}

// Run the generation
if (require.main === module) {
  generateFavicons();
}
