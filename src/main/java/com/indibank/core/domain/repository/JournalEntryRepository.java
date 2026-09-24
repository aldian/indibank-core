package com.indibank.core.domain.repository;

import com.indibank.core.domain.model.JournalEntry;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface JournalEntryRepository extends JpaRepository<JournalEntry, Long> {

    @Query("SELECT j FROM JournalEntry j WHERE j.account.accountNumber = :accountNumber ORDER BY j.createdAt DESC")
    List<JournalEntry> findByAccountNumberOrderByCreatedAtDesc(@Param("accountNumber") String accountNumber, Pageable pageable);

    List<JournalEntry> findByTransferId(Long transferId);
}
