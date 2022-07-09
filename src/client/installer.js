const installer = require('electron-installer-debian')
 
const options = {
  src: 'builds/docker-dashboard-linux-x64/',
  dest: 'builds/',
  arch: 'amd64',
  icon: {
    '48x48': 'src/assets/icons/Icon48.png',
    '64x64': 'src/assets/icons/Icon64.png',
    '128x128': 'src/assets/icons/Icon128.png',
    '256x256': 'src/assets/icons/Icon256.png',
    'scalable': 'src/assets/icons/Icon.svg'
  },
}
 
async function main (options) {
  console.log('Creating package (this may take a while)')
  try {
    await installer(options)
    console.log(`Successfully created package at ${options.dest}`)
  } catch (err) {
    console.error(err, err.stack)
    process.exit(1)
  }
}

main(options)