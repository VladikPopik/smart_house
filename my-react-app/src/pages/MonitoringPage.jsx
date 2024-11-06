import Monitoring from '../components/Monitoring';
import AppBarComponent from '../components/AppBarComponent.jsx';
import MonitoringCharts from '../components/MonitoringLayoutGraphs.jsx';


export default function MonitoringPage() {
    return (
        <body>
            <AppBarComponent/>
            <Monitoring />
            <MonitoringCharts />
        </body>
    );
}