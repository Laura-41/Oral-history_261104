import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.neo4j.dbms.api.DatabaseManagementService;
import org.neo4j.dbms.api.DatabaseManagementServiceBuilder;
import org.neo4j.configuration.connectors.BoltConnector;
import org.neo4j.configuration.connectors.HttpConnector;
import org.neo4j.configuration.connectors.HttpsConnector;
import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.Result;
import org.neo4j.graphdb.Transaction;

/** Offline importer and verifier for the isolated oral-history Neo4j demo. */
public final class EmbeddedNeo4jRunner {
    private static final Path DEMO_HOME = Path.of("/tmp/oral_history_neo4j_home");
    private static final Path CONFIG = Path.of("/tmp/oral_history_neo4j_demo/conf/neo4j.conf");
    private static final Path IMPORT_SCRIPT = Path.of("/tmp/oral_history_neo4j_demo/import.cypher");
    private static final Path REPORT = Path.of("/tmp/oral_history_neo4j_demo/reports/verification_report.txt");

    private EmbeddedNeo4jRunner() {}

    private static List<String> statements(Path path) throws IOException {
        String source = Files.readString(path, StandardCharsets.UTF_8)
                .replace("\r\n", "\n")
                .replace("\r", "\n");
        StringBuilder cleaned = new StringBuilder();
        for (String line : source.split("\n", -1)) {
            String trimmed = line.stripLeading();
            if (!trimmed.startsWith("//")) {
                cleaned.append(line).append('\n');
            }
        }
        List<String> result = new ArrayList<>();
        for (String statement : cleaned.toString().split(";")) {
            if (!statement.isBlank()) {
                result.add(statement.trim());
            }
        }
        return result;
    }

    private static void execute(GraphDatabaseService db, String statement) {
        try (Transaction tx = db.beginTx(); Result ignored = tx.execute(statement)) {
            while (ignored.hasNext()) {
                ignored.next();
            }
            tx.commit();
        }
    }

    private static String query(GraphDatabaseService db, String title, String cypher) {
        StringBuilder output = new StringBuilder();
        output.append("\n=== ").append(title).append(" ===\n");
        try (Transaction tx = db.beginTx(); Result result = tx.execute(cypher)) {
            List<String> columns = result.columns();
            output.append(String.join("\t", columns)).append('\n');
            while (result.hasNext()) {
                Map<String, Object> row = result.next();
                for (int i = 0; i < columns.size(); i++) {
                    if (i > 0) output.append('\t');
                    Object value = row.get(columns.get(i));
                    output.append(value == null ? "" : value.toString().replace('\n', ' '));
                }
                output.append('\n');
            }
            tx.commit();
        }
        return output.toString();
    }

    public static void main(String[] args) throws Exception {
        DatabaseManagementService management = new DatabaseManagementServiceBuilder(DEMO_HOME)
                .loadPropertiesFromFile(CONFIG)
                .setConfig(BoltConnector.enabled, false)
                .setConfig(HttpConnector.enabled, false)
                .setConfig(HttpsConnector.enabled, false)
                .build();
        Runtime.getRuntime().addShutdownHook(new Thread(management::shutdown));
        GraphDatabaseService db = management.database("neo4j");

        try {
            List<String> importStatements = statements(IMPORT_SCRIPT);
            int index = 0;
            for (String statement : importStatements) {
                index++;
                try {
                    execute(db, statement);
                } catch (RuntimeException error) {
                    throw new RuntimeException("Import failed at statement " + index + ":\n" + statement, error);
                }
            }

            StringBuilder report = new StringBuilder();
            report.append("Neo4j oral-history development-corpus verification\n");
            report.append("import_statements=").append(importStatements.size()).append('\n');
            report.append(query(db, "节点总数", "MATCH (n) RETURN count(n) AS nodes"));
            report.append(query(db, "关系总数", "MATCH ()-[r]->() RETURN count(r) AS relationships"));
            report.append(query(db, "各类节点", "MATCH (n) UNWIND labels(n) AS label RETURN label, count(*) AS count ORDER BY count DESC, label"));
            report.append(query(db, "各类关系", "MATCH ()-[r]->() RETURN type(r) AS relationship, count(*) AS count ORDER BY count DESC, relationship"));
            report.append(query(db, "事件链", "MATCH (d:InterviewDocument)-[:HAS_EVENT]->(e:EventNode) OPTIONAL MATCH (e)-[:HAS_TIME]->(t:EventTime) RETURN d.interviewee AS person, e.historical_order AS event_order, e.event_name AS event, t.normalized_start AS start ORDER BY person, event_order"));
            report.append(query(db, "共享实体", "MATCH (d:InterviewDocument)-[:HAS_SEGMENT]->(:SourceSegment)-[:HAS_MENTION]->(:EntityMention)-[:MENTIONS]->(e:Entity) WITH e, collect(DISTINCT d.interviewee) AS people, count(*) AS mentions WHERE size(people)>1 RETURN e.canonical_name AS entity, people, mentions ORDER BY mentions DESC, entity"));
            report.append(query(db, "原文覆盖", "MATCH (d:InterviewDocument)-[:HAS_COVERAGE_AUDIT]->(a:CoverageAudit) RETURN d.interviewee AS person, a.total_segments AS segments, a.attached_segments AS attached, a.coverage_rate AS coverage"));
            report.append(query(db, "人工已核验但现实指称仍不确定的实体", "MATCH (e:Entity {review_status:'CONFIRMED'}) WHERE e.authority_status IN ['TRANSCRIPTION_UNCERTAIN','UNRESOLVED'] RETURN e.canonical_name AS entity, e.review_status AS review_status, e.authority_status AS authority_status ORDER BY entity"));
            report.append(query(db, "全文时间表达", "MATCH (d:InterviewDocument)-[:HAS_SEGMENT]->(s:SourceSegment)-[:HAS_TIME_EXPRESSION]->(t:TimeExpression) RETURN d.interviewee AS person, s.source_part AS source_part, count(t) AS expressions ORDER BY person, source_part"));
            report.append(query(db, "脚注时间表达", "MATCH (d:InterviewDocument)-[:HAS_SEGMENT]->(s:SourceSegment)-[:HAS_TIME_EXPRESSION]->(t:TimeExpression) WHERE s.source_part='footnotes' RETURN d.interviewee AS person, t.raw_text AS raw_text, t.normalized_start AS normalized_start ORDER BY person, normalized_start"));
            Files.writeString(REPORT, report.toString(), StandardCharsets.UTF_8);
            System.out.print(report);
        } finally {
            management.shutdown();
        }
    }
}

