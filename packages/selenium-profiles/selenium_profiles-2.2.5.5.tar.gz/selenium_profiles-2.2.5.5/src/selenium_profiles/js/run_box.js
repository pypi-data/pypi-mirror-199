function delay(time) {
  return new Promise(resolve => setTimeout(resolve, time*1000));
}
function start_section(section){
    document.getElementsByTagName('colab-run-button')[section].click()
}
delay(10).then(() => start_section(4));