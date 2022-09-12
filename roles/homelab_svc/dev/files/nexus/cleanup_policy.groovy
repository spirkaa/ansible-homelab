// https://github.com/idealista/nexus-role/blob/master/files/scripts/cleanup_policy.groovy
import groovy.json.JsonSlurper
import java.util.concurrent.TimeUnit

import org.sonatype.nexus.cleanup.storage.CleanupPolicyStorage
import com.google.common.collect.Maps

import static org.sonatype.nexus.repository.search.DefaultComponentMetadataProducer.IS_PRERELEASE_KEY
import static org.sonatype.nexus.repository.search.DefaultComponentMetadataProducer.LAST_BLOB_UPDATED_KEY
import static org.sonatype.nexus.repository.search.DefaultComponentMetadataProducer.LAST_DOWNLOADED_KEY
import static org.sonatype.nexus.repository.search.DefaultComponentMetadataProducer.REGEX_KEY


def cleanupPolicyStorage = container.lookup(CleanupPolicyStorage.class.getName())

parsed_args = new JsonSlurper().parseText(args)
Map<String, String> criteriaMap = createCriteria(parsed_args)

if (cleanupPolicyStorage.exists(parsed_args.name)) {
    existingPolicy = cleanupPolicyStorage.get(parsed_args.name)
    existingPolicy.setNotes(parsed_args.notes)
    existingPolicy.setCriteria(criteriaMap)
    cleanupPolicyStorage.update(existingPolicy)
} else {
    format = parsed_args.format == "all" ? "ALL_FORMATS" : parsed_args.format
    cleanupPolicy = cleanupPolicyStorage.newCleanupPolicy()
    cleanupPolicy.setName(parsed_args.name)
    cleanupPolicy.setNotes(parsed_args.notes)
    cleanupPolicy.setFormat(format)
    cleanupPolicy.setMode('deletion')
    cleanupPolicy.setCriteria(criteriaMap)

    cleanupPolicyStorage.add(cleanupPolicy)
}

def Map<String, String> createCriteria(args) {
    Map<String, String> criteriaMap = Maps.newHashMap()
    if (args.published_before == null) {
        criteriaMap.remove(LAST_BLOB_UPDATED_KEY)
    } else {
        criteriaMap.put(LAST_BLOB_UPDATED_KEY, asStringSeconds(args.published_before))
    }
    if (args.last_download_before == null) {
        criteriaMap.remove(LAST_DOWNLOADED_KEY)
    } else {
        criteriaMap.put(LAST_DOWNLOADED_KEY, asStringSeconds(args.last_download_before))
    }
    if ((args.is_pre_release == null) || (args.is_pre_release == "")) {
        criteriaMap.remove(IS_PRERELEASE_KEY)
    } else {
        criteriaMap.put(IS_PRERELEASE_KEY, Boolean.toString(args.is_pre_release == "PRERELEASES"))
    }
    if ((args.regex_key == null) || (args.regex_key == "")) {
        criteriaMap.remove(REGEX_KEY)
    } else {
        criteriaMap.put(REGEX_KEY, String.valueOf(args.regex_key))
    }
    return criteriaMap
}

def Integer asSeconds(days) {
    return days * TimeUnit.DAYS.toSeconds(1)
}

def String asStringSeconds(daysString) {
    return String.valueOf(asSeconds(Integer.parseInt(daysString)))
}
