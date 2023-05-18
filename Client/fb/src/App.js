// React Imports
import './App.css';

// My imports
import CurWaterLevel from './CurWaterLevel.js';
import WaterChart from './WaterChart.js';

function App() {
  return (
    <div>
      <h1>Fountain Brain</h1>
      <CurWaterLevel />
      <WaterChart />
    </div>
  );
}

export default App;
