import AppBarComponent from '../components/AppBarComponent.jsx';
import BudgetTable from '../components/BudgetTableComponent.jsx';


export default function BudgetPage () {
    return (
        <div>
            <AppBarComponent/>
            <BudgetTable></BudgetTable>
        </div>
    )
}