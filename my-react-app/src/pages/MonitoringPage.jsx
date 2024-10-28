import Monitoring from '../components/Monitoring';
import AppBarComponent from '../components/AppBarComponent.jsx';
import MonitoringCharts from '../components/MonitoringLayoutGraphs.jsx';


export default function MonitoringPage() {
    return (
        <body>
            <AppBarComponent/>
            <Monitoring />
            <MonitoringCharts />
            {/* <iframe src='${config.protocol}://127.0.0.1:8000/monitoring' className='full_screen'></iframe> */}
        </body>
    );
}