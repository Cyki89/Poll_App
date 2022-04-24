import TableHeaders from "./TableHeaders";
import TableBody from "./TableBody";

const Table = ({ columns, data, sortOrder, sortColumn, onSort }) => {
  return (
    <table>
      <TableHeaders
        columns={columns}
        sortOrder={sortOrder}
        sortColumn={sortColumn}
        onSort={onSort}
      />
      <TableBody columns={columns} data={data} />
    </table>
  );
};

export default Table;
