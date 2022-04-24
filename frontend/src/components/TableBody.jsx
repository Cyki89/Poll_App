const renderCell = (item, column, idx) => {
  if (column.content) return column.content(item, idx);

  const pathItems = column.path.split(".");

  let newItem = { ...item };
  for (let i = 0; i < pathItems.length; ++i) {
    newItem = newItem[pathItems[i]];
  }

  return newItem;
};

const createKey = (idx, column) => `${idx}${column.path}`;

const TableBody = ({ columns, data }) => {
  return (
    <tbody>
      {data.map((item, idx) => (
        <tr key={idx}>
          {columns.map((column) => (
            <td key={createKey(idx, column)}>
              {renderCell(item, column, idx)}
            </td>
          ))}
        </tr>
      ))}
    </tbody>
  );
};

export default TableBody;
