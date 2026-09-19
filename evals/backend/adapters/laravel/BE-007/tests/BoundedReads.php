<?php
namespace Reviewer;

/** Observe actual PDO result rows; no SQL-string matching or query re-execution.
 * Laravel select/selectOne use fetchAll; cursor uses fetch. The SQLite fixture
 * connection is instrumented only during the request and restored in finally.
 */
class BE007ReadStatement extends \PDOStatement
{
    public static array $reads = [];
    private ?int $observation = null;
    protected function __construct() {}
    private function observed(int $rows): void {
        if ($this->observation === null) {
            $this->observation = count(self::$reads);
            self::$reads[] = ['sql'=>$this->queryString,'rows'=>0];
        }
        self::$reads[$this->observation]['rows'] += $rows;
    }
    public function fetchAll(int $mode = \PDO::FETCH_DEFAULT, mixed ...$args): array {
        $rows=parent::fetchAll($mode,...$args);$this->observed(count($rows));return $rows;
    }
    public function fetch(int $mode = \PDO::FETCH_DEFAULT, int $orientation = \PDO::FETCH_ORI_NEXT, int $offset = 0): mixed {
        $row=parent::fetch($mode,$orientation,$offset);$this->observed($row===false?0:1);return $row;
    }
    public function fetchColumn(int $column = 0): mixed {
        $value=parent::fetchColumn($column);$this->observed($value===false?0:1);return $value;
    }
}
trait BE007BoundedReads
{
    private function measuredRead(string $path, int $size, int $overhead): array {
        $pdo=\Illuminate\Support\Facades\DB::connection()->getPdo();
        $original=$pdo->getAttribute(\PDO::ATTR_STATEMENT_CLASS);
        BE007ReadStatement::$reads=[];
        $pdo->setAttribute(\PDO::ATTR_STATEMENT_CLASS,[BE007ReadStatement::class]);
        try { $response=$this->req('GET',$path)->assertOk(); }
        finally { $pdo->setAttribute(\PDO::ATTR_STATEMENT_CLASS,$original); }
        $reads=BE007ReadStatement::$reads;
        $this->assertNotEmpty($reads,'PDO read measurement must execute');
        $total=array_sum(array_column($reads,'rows'));
        fwrite(STDOUT,"\nREAD_EVIDENCE ".json_encode(['path'=>$path,'page_size'=>$size,'total_rows'=>$total,'reads'=>$reads])."\n");
        foreach($reads as $read) $this->assertLessThanOrEqual($size,$read['rows'],'Unbounded database result: '.$read['sql']);
        $this->assertLessThanOrEqual($size+$overhead,$total,'Total fetched rows exceed page plus fixed fixture overhead');
        return [$response,$reads];
    }
}
