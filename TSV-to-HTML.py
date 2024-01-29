def read_tsv_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            row = line.strip().split('\t')
            data.append(row)
    return data

def bytes_to_megabytes(bytes_value):
    megabytes = bytes_value / (1024 * 1024)
    return round(megabytes)

def generate_html_table_transposed(data, output_file):
    with open(output_file, 'w') as file:
        file.write('''<!DOCTYPE html>
<html>
<head>
<style>
table {
  border-collapse: collapse;
  width: 100%;
}
th, td {
  border: 1px solid black;
  padding: 8px;
}
</style>
</head>
<body>
<table>
''')

        num_rows = len(data)
        num_cols = len(data[0])

        # Write table headers
        file.write('<tr>\n')
        for i in range(num_rows):
            file.write(f'  <th>{data[i][0]}</th>\n')
        file.write('</tr>\n')

        # Write table rows (transposed as columns)
        for j in range(1, num_cols):
            file.write('<tr>\n')
            for i in range(num_rows):
                if (j == 3 and i != 0):
                    file.write(f'  <td><a href="{data[i][j]}">Download</a></td>\n')
                elif (j == 4 and i != 0):
                    file.write(f'  <td class="clickable-td">{data[i][j]}</td>\n')
                elif (j == 8 and i != 0):
                    if (data[i][j]).strip(): # Check if the cell is not empty
                        megabytes = bytes_to_megabytes(int(data[i][j]))
                        file.write(f'  <td>{megabytes} MB</td>\n')
                else:
                    file.write(f'  <td>{data[i][j]}</td>\n')
            file.write('</tr>\n')

        file.write('''</table>
<script>
  // Function to copy the text inside the clicked <td> to the clipboard
  function copyToClipboard(text) {
      const el = document.createElement("textarea");
      el.value = text;
      document.body.appendChild(el);
      el.select();
      document.execCommand("copy");
      document.body.removeChild(el);
  }
  
  // Add click event listeners to the clickable <td> elements
  const clickableTds = document.querySelectorAll(".clickable-td");
  clickableTds.forEach((td) => {
      td.addEventListener("click", () => {
      const textToCopy = td.textContent;
      copyToClipboard(textToCopy);
      alert("Text copied to clipboard: " + textToCopy);
      });
  });
</script>
</body>
</html>
''')

import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        script_name = sys.argv[0]
        print(f"Usage: python {script_name} path-to-TSV-file")
        sys.exit(1)
    input_tsv_file = sys.argv[1]  # Replace with the path to your TSV file
    output_html_file = "PSV.html"  # Replace with the desired output HTML file path
    table_data = read_tsv_file(input_tsv_file)
    generate_html_table_transposed(table_data, output_html_file)
