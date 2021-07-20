const DEFAULT_GROW_HOURS = 4;

let torchState = false;
let setTorch;

let consoleDiv;
let startTime;
let nCycles;
let onMinutes;
let offMinutes;

window.onload = async () => {
  consoleDiv = document.getElementById('console-div');
  print('Console test ok. ');
  try {
    setTorch = await initTorch();
  } catch(e) {
    print(e);
    console.error(e);
  }
  startTime = document.getElementById('start-time');
  const date = new Date();
  date.setHours(date.getHours() + DEFAULT_GROW_HOURS);
  startTime.value = `${
    date.getFullYear()
  }-${
    (date.getMonth() + 1).toString().padStart(2, '0')
  }-${
    date.getDate().toString().padStart(2, '0')
  }T${
    date.getHours().toString().padStart(2, '0')
  }:${
    date.getMinutes().toString().padStart(2, '0')
  }`;
  startTime.addEventListener('input', onStartTimeChange);
  startTime.hidden = false;
  onStartTimeChange({ target: startTime });

  nCycles    = document.getElementById('n-cycles');
  onMinutes  = document.getElementById('on-minutes');
  offMinutes = document.getElementById('off-minutes');
};

const print = (msg) => {
  consoleDiv.innerHTML += msg + '<br />';
};

const initTorch = async () => {
  if (! 'mediaDevices' in navigator) {
    print(`Browser doesn't support. Use Chrome. `);
    return;
  }
  alert('Please allow camera access for me to control the torch.');
  const stream = await navigator.mediaDevices.getUserMedia({
    video: {
      facingMode: 'environment',
    }, 
  });
  const track = stream.getVideoTracks()[0];
  return (state) => {
    if (torchState !== state) {
      track.applyConstraints({
        advanced: [{torch: state}], 
      }).catch((e) => {
        print(e);
        console.error(e);
      });
      print(`Torch: ${state}`);
      torchState = state;
    }
  };
};

const onStartTimeChange = (e) => {
  const target = new Date(e.target.value);
  const delta = target - new Date();
  const delta_hours = delta / 1000 / 60 / 60;
  const deltaDisplay = document.getElementById('start-time-delta');
  deltaDisplay.innerText = `i.e., ${
    Math.round(delta_hours * 100) / 100
  } hours later.`;
};

const testTorch = () => {
  if (setTorch === undefined) {
    alert('Torch not initialized yet.');
    return;
  }
  setTorch(! torchState);
};

const confirm = () => {
  setTorch(false);
  document.getElementById('panel').hidden = true;
  const start_time = new Date(startTime.value);
  const n_cycles = Math.round(nCycles.value);
  const on_minutes  = Math.round(onMinutes.value);
  const off_minutes = Math.round(offMinutes.value);
  print('Sequence will start at:');
  print(start_time);
  print('Sequence:');
  const sum_minutes = on_minutes + off_minutes;
  const total_minutes = sum_minutes * n_cycles;
  print(`${n_cycles} × ( ${on_minutes} + ${off_minutes} = ${sum_minutes} ) = ${total_minutes}.`);
  print('Sequence will end at:');
  const end_time = new Date(start_time);
  end_time.setMinutes(end_time.getMinutes() + total_minutes);
  print(end_time);
  const interval = setInterval(() => {
    const progress = (new Date() - start_time) / (1000 * 60);
    if (progress < 0) return;
    const cycle_i = Math.floor(progress / sum_minutes);
    if (cycle_i >= n_cycles) {
      clearInterval(interval);
      print('Sequence finished at:');
      print(new Date());
      return;
    }
    const residual = progress - cycle_i * sum_minutes;
    setTorch(residual < on_minutes);
  }, 1000);
};
